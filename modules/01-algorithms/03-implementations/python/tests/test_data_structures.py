from src.data_structures.segment_tree_sum import SegmentTreeSum
from src.data_structures.union_find import UnionFind


def test_union_find():
    uf = UnionFind(5)
    assert not uf.connected(0, 1)
    assert uf.union(0, 1)
    assert uf.connected(0, 1)
    assert not uf.union(0, 1)


def test_segment_tree_sum():
    st = SegmentTreeSum([1, 3, 5, 7, 9, 11])
    assert st.query(1, 4) == 15
    st.update(2, 6)
    assert st.query(1, 4) == 16
    assert st.query(0, 6) == 37
