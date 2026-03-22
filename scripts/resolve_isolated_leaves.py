import json
import os
import sys

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(repo_root, "docs", "archive")
    
    with open(os.path.join(docs_dir, "content-index.json"), "r") as f:
        content_index = json.load(f)
        
    with open(os.path.join(docs_dir, "relations.json"), "r") as f:
        relations_index = json.load(f)
        
    with open(os.path.join(docs_dir, "quality-report.json"), "r") as f:
        quality_report = json.load(f)

    # create lookup maps
    items_by_id = {item["id"]: item for item in content_index["items"]}
    
    # We only want to process the known zero_outgoing_link_ids_sample 
    # Or actually, let's just process all 370 of them
    zero_out = quality_report["issues"]["zero_outgoing_link_ids_sample"]
    
    # To get ALL 370, we can just iterate. The sample only has 50.
    # The real zero_outgoing_links count is in counts.
    # We can compute it ourselves from relations.json:
    zero_out_ids = [
        doc_id for doc_id, rel in relations_index["documents"].items()
        if len(rel["outgoing_links"]) == 0
    ]
    
    modified_count = 0
    
    for doc_id in zero_out_ids:
        # Skip if it is a hub page or not found
        item = items_by_id.get(doc_id)
        if not item:
            continue
            
        if item["content_type"] in {"module-overview", "project", "track", "doc"}:
            continue  # Don't touch hubs, just leaves.
            
        rels = relations_index["documents"].get(doc_id, {})
        related = rels.get("related", [])
        
        # Filter related items to prefer same-module siblings
        # Exclude backlinks (which point back to the README hub), we want lateral links
        candidates = [r for r in related if r["type"] not in ("backlink",)]
        
        # Sort by weight descending
        candidates.sort(key=lambda x: x["weight"], reverse=True)
        
        # Take top 3
        top_candidates = candidates[:3]
        if not top_candidates:
            # Fallback to backlink if no siblings exist
            candidates = [r for r in related]
            candidates.sort(key=lambda x: x["weight"], reverse=True)
            top_candidates = candidates[:3]
            
        if not top_candidates:
            continue
            
        # Build the injected markdown section
        source_path_abs = os.path.join(repo_root, item["path"])
        source_dir = os.path.dirname(source_path_abs)
        
        links_markdown = []
        for c in top_candidates:
            target_item = items_by_id.get(c["id"])
            if not target_item:
                continue
            
            target_path_abs = os.path.join(repo_root, target_item["path"])
            rel_path = os.path.relpath(target_path_abs, source_dir)
            links_markdown.append(f"- [{target_item['title']}]({rel_path})")
            
        if not links_markdown:
            continue
            
        injection = "\n\n## Related Concepts\n\n" + "\n".join(links_markdown) + "\n"
        
        # Read file, append, write back
        try:
            with open(source_path_abs, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Avoid double injection
            if "## Related Concepts" in content:
                continue
                
            # Ensure file ends with newline before appending
            if not content.endswith("\n"):
                content += "\n"
                
            content += injection
            
            with open(source_path_abs, "w", encoding="utf-8") as f:
                f.write(content)
                
            modified_count += 1
        except Exception as e:
            print(f"Failed to modify {source_path_abs}: {e}")
            
    print(f"Successfully injected semantic Related Concepts links into {modified_count} isolated leaf pages.")

if __name__ == "__main__":
    main()
