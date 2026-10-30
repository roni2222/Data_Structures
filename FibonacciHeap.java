



public class FibonacciHeap
{
	public HeapNode minNode;

	public int size_property;
	public int num_trees;

	public int cutsCounter = 0;
	public int linksCounter = 0;

	public static int counter = 0;



	//O(1) - time complexity
	public FibonacciHeap()
	{
		this.minNode = null;
		this.size_property = 0;
	}


	/**
	 *
	 * pre: key > 0
	 *
	 * Insert (key,info) into the heap and return the newly generated HeapNode.
	 *
	 */
	//worst case - O(n), amortized - O(logn)
	private void consolidate(){
		int arraySize = (int) Math.ceil(Math.log(size_property) / Math.log(2));
		HeapNode[] buckets = new HeapNode[arraySize];

		//Place all roots into the buckets array
		HeapNode start = minNode;
		HeapNode current = minNode;

		do {
			HeapNode x = current;
			current = current.next;
			int degree = x.rank;

			while (buckets[degree] != null) {
				HeapNode y = buckets[degree];

				if (y.key < x.key) {
					HeapNode temp = x;
					x = y;
					y = temp;
				}
				link(y,x);
				buckets[degree] = null;
				degree++;
			}
			buckets[degree] = x;
		} while (current != start);

		// Reconstruct the root list and find the new minimum
		this.minNode = null;

		int first_index_bucket = 0;
		int last_index_bucket = 0;
		int last_visited = 0;
		for (int i = 0; i < buckets.length; i++) {
			if (buckets[i] != null) {
				if (this.minNode == null) {
					this.minNode = buckets[i];
					buckets[i].next = buckets[i];
					buckets[i].prev = buckets[i];
					first_index_bucket = i;
					last_visited = i;
				}
				else {
					if (last_visited != i){
						buckets[last_visited].next = buckets[i];
						buckets[i].prev = buckets[last_visited];
						last_visited = i;
					}
					if (buckets[i].key < this.minNode.key) {
						this.minNode = buckets[i];
					}
				}
				last_index_bucket = i;
			}
		}

		if(buckets[first_index_bucket] != null && buckets[last_index_bucket] != null){
			buckets[first_index_bucket].prev = buckets[last_index_bucket];
			buckets[last_index_bucket].next = buckets[first_index_bucket];
		}


	}

	// Add a node to the root list
	//Time complexity - O(1)
	private void addToRootList(HeapNode node) {

		if (this.minNode == null) {
			this.minNode = node;
			node.next = node;
			node.prev = node;
		}
		else {
			mergeRootLists(this.minNode, node);
		}
	}

	// Merge two circular doubly linked lists
	//Time complexity - O(1)
	private void mergeRootLists(HeapNode a, HeapNode b) {
		if (a == null || b == null) {
			return;
		}
		HeapNode aNext = a.next;
		HeapNode bPrev = b.prev;
		a.next = b;
		b.prev = a;
		aNext.prev = bPrev;
		bPrev.next = aNext;
	}

	//complexity - O(1)
	public HeapNode insert(int key, String info)
	{
		HeapNode node = new HeapNode(key, info);

		// Add the node as a root
		if (this.minNode == null) { //The tree is empty
			this.minNode = node;
			this.minNode.next = this.minNode;
			this.minNode.prev = this.minNode;
		}
		else {
			this.minNode.addSibling(node);
		}

		this.size_property++;
		this.num_trees++;

		// checking if the new node is the minimum
		if (node.key < this.minNode.key) {
			this.minNode = node;
		}

		node.val = Integer.toString(counter);

		counter++;

		return node;
	}

	/**
	 *
	 * Return the minimal HeapNode, null if empty.
	 *
	 */
	//Time Complexity - O(1)
	public HeapNode findMin()
	{
		return this.minNode;
	}

	/**
	 *
	 * Delete the minimal item
	 *
	 */
	//worst case - O(n), amortized - O(logn)
	public void deleteMin()
	{
		//empty heap
		if (this.minNode == null) {
			return;
		}

		int rank_min = minNode.rank;
		HeapNode min = this.minNode;

		this.cutsCounter += minNode.rank;

		// add x children to the root list
		if (min.child != null) {
			HeapNode child = min.child;
			do {
				child.parent = null; // Disconnect child from its parent
				child = child.next;
			} while (child != min.child);

			// Merge the children of x with the root list
			mergeRootLists(this.minNode, min.child);
		}


		// only one node in heap
		if (min == min.next) {
			this.minNode = null;
		}
		else {
			min.prev.next = min.next;
			min.next.prev = min.prev;
			this.minNode = min.next; // Meanwhile the min is the next node
			consolidate(); //consolidate (in this method we find the new min)
		}

		this.size_property--;
		this.num_trees = this.num_trees - 1 + rank_min;

	}


	/**
	 *
	 * pre: 0<diff<x.key
	 *
	 * Decrease the key of x by diff and fix the heap.
	 *
	 */
	//worst case - O(n), amortized - O(1)
	public void decreaseKey(HeapNode x, int diff)
	{
		if (x == null){
			return;
		}

		x.key -= diff;

		if (x.parent == null) { //no heap property violation
			if (x.key < this.minNode.key) {
				this.minNode = x;
			}
			return;
		}

		if (x.key < x.parent.key) { //heap property violation
			cascadingCut(x);
		}
	}

	/**
	 * `
	 * Delete the x from the heap.
	 *
	 */
	//worst case - O(n), amortized - O(logn)
	public void delete(HeapNode x)
	{
		if(x == null){
			return;
		}
		if(x == this.minNode){
			deleteMin();
		}
		else {
			int x_rank = x.rank;
			boolean has_parent = x.parent != null;

			if(x.parent != null){
				this.cascadingCut(x);
				this.num_trees --; //after cascading the node we delete is considered as additional root

			}
			else {
				this.cutsCounter += x.rank;
			}

			// Remove x from its siblings
			x.removeFromSiblings();

			// add x children to the root list
			if (x.child != null) {
				HeapNode child = x.child;
				do {
					child.parent = null; // Disconnect child from its parent
					child = child.next;
				} while (child != x.child);

				// Merge the children of x with the root list
				mergeRootLists(this.minNode, x.child);
			}


			this.size_property--;

			this.num_trees += x_rank;

			if(!has_parent){
				this.num_trees --;
			}

		}
	}


	/**
	 *
	 * Return the total number of links.
	 *
	 */
	//Time Complexity - O(1)
	public int totalLinks()
	{
		return linksCounter;
	}


	/**
	 *
	 * Return the total number of cuts.
	 *
	 */
	//Time Complexity - O(1)
	public int totalCuts()
	{
		return cutsCounter;
	}


	/**
	 *
	 * Meld the heap with heap2
	 *
	 */
	//Time Complexity - O(1)
	public void meld(FibonacciHeap heap2)
	{
		if (heap2 == null){
			return;
		}
		this.minNode.next.prev = heap2.minNode.prev;
		heap2.minNode.prev.next = minNode.next;
		this.minNode.next = heap2.minNode;
		heap2.minNode.prev = minNode;

		// Find the new minimum from both heaps
		if (heap2.minNode.key < this.minNode.key) {
			this.minNode = heap2.minNode;
		}

		this.num_trees += heap2.num_trees;
		this.size_property += heap2.size_property;
		this.cutsCounter += heap2.cutsCounter;
		this.linksCounter += heap2.linksCounter;
	}


	/**
	 *
	 * Return the number of elements in the heap
	 *
	 */

	//Time Complexity - O(1)
	public int size()
	{
		return this.size_property;
	}


	/**
	 *
	 * Return the number of trees in the heap.
	 *
	 */

	//Time Complexity - O(1)
	public int numTrees()
	{
		return this.num_trees;
	}

	//Time Complexity - O(1)
	// cascadingCut using this method
	private void cut(HeapNode node) {
		cutsCounter++;
		node.mark = false;
		node.removeFromSiblings();
		this.minNode.addSibling(node);
		this.num_trees++;
		node.parent = null;
		if (node.key < this.minNode.key){
			this.minNode = node;
		}
	}

	//Help Method - decreaseKey uses cascadingCut in case of heap property violation
	//worst case - O(logn), amortized - O(1)
	private void cascadingCut(HeapNode node) {
		HeapNode parent = node.parent;
		cut(node);
		if (parent.parent != null) {
			if (!parent.mark) {
				parent.mark = true;
			}
			else {
				cascadingCut(parent);
			}
		}
	}

	//Helper Method - Time complexity O(1)
	private HeapNode link(HeapNode node1, HeapNode node2) {
		linksCounter++;
		HeapNode child;
		HeapNode parent;
		if (node1.key > node2.key || (node1.key == node2.key && node1.val.compareTo(node2.val) != 0)) {
			child = node1;
			parent = node2;
		}
		else {
			child = node2;
			parent = node1;
		}
		parent.addChild(child);
		this.num_trees --;
		return parent;
	}

	/**
	 * Class implementing a node in a Fibonacci Heap.
	 *
	 */
	public static class HeapNode{
		public int key;
		public String info;
		public HeapNode child;
		public HeapNode next;
		public HeapNode prev;
		public HeapNode parent;
		public int rank;
		public boolean mark;

		public String val;

		//complexity: O(1)
		public HeapNode(int key, String info){
			this.key = key;
			this.info = info;
			this.next = this;
			this.prev = this;
			this.child = null;
			this.parent = null;
			this.rank = 0;
			this.mark = false;
		}

		//Helper Method - Time complexity O(1)
		private void addChild(HeapNode node) {
			node.parent = this;
			if (child == null) {
				child = node;
				node.next = node;
				node.prev = node;
				this.rank++;
			}
			else {
				child.addSibling(node);
			}
		}

		// Helper Method - O(1)
		private void addSibling(HeapNode sibling) {
			sibling.next = this.next;
			this.next.prev = sibling;
			if (this.parent != null) { //not relevant for insert
				this.parent.rank++;
			}
			sibling.prev = this;
			this.next = sibling;
		}


		// Helper Method - Time Complexity O(1)
		private void removeFromSiblings() {
			if (this.next == this) {
				if (this.parent != null) {
					this.parent.child = null;
					this.parent.rank--;
				}
			}
			else { //node has a sibling
				if (this.parent != null) {
					if (this.parent.child == this) {
						this.parent.child = this.next;
					}
					this.parent.rank--;
				}
				this.next.prev = this.prev;
				this.prev.next = this.next;
			}
		}

	}
}
