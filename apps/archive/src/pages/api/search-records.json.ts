import { archiveItems, searchIndex } from "../../lib/archive";

export async function GET() {
  const records = searchIndex.documents.map((doc) => {
    const item = archiveItems.find((candidate) => candidate.id === doc.id);
    return {
      ...doc,
      status: item?.status ?? "",
      format: item?.format ?? "",
      module_title: item?.module?.title ?? "",
      track_titles: item?.tracks ?? []
    };
  });

  return new Response(JSON.stringify(records), {
    headers: { "Content-Type": "application/json" }
  });
}
