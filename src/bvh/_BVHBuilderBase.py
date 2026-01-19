class BVHBuilderBase:
    _is_parallel: bool

    def __init__(
        self, leaf_node_size: int, max_tree_depth: int, is_parallel: bool = False
    ):
        self._is_parallel = is_parallel
        self._leaf_node_size = leaf_node_size
        self._max_tree_depth = max_tree_depth

    @property
    def max_tree_depth(self) -> int:
        """Get the maximum depth of the BVH tree."""
        raise NotImplementedError("Subclasses must implement this method.")

    @property
    def leaf_node_size(self) -> int:
        """Get the maximum number of primitives in a leaf node."""
        raise NotImplementedError("Subclasses must implement this method.")

    @property
    def is_parallel(self) -> bool:
        """Check if the BVH builder operates in parallel mode."""
        return self._is_parallel

    @is_parallel.setter
    def is_parallel(self, value: bool):
        """Set the parallel mode of the BVH builder."""
        self._is_parallel = value
