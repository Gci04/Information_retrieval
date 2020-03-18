class Node {
		constructor(key, value, level) {
			this.key = key;
			this.value = value;
			this.next = [];
			if (level) this.next.length = level;
		}
}
class SkipList {

	constructor(scale) {
		this.MAXLEN = 2000000;
		this.p = scale;
		// estimate levels
		this.levels = parseInt(Math.round(Math.log(this.MAXLEN) / Math.log(this.p)));
		
		// guard elements
		this.start = new Node(Number.NEGATIVE_INFINITY, null, this.levels);
		this.end = new Node(Number.POSITIVE_INFINITY, null, 0);
		for (var l = 0; l < this.start.next.length; l++)
			this.start.next[l] = this.end;
	}
	
	up() { return Math.random() > (1 / this.p); }
	randomlevel() {
		var l = 1;
		while (this.up() && l < this.levels) l++;
		return l;
	}
	
	find(key) {
		var current = this.start;
		var level = this.levels - 1;

		while (level >= 0) {
			// move forward on the level
			while (current.next[level].key < key) {
				current = current.next[level];
			}
			
			// our next on this level is greater, than key
			if (current.key == key) return current;
			
			// go down to find smaller
			for (; level >= 0; --level) {
				if (current.next[level].key <= key) {
					current = current.next[level];
					break;
				}
			}
		}
		return null;
	}

	findPrevs(key) {
		
		var prev = [];
		var level = this.levels - 1;
		// start searching from top left corner
		prev[level] = this.start;
		
		while (level >= 0) {
			// move forward on the level while next element is smaller than key
			while (prev[level].next[level].key < key) {
				prev[level] = prev[level].next[level];
			}
			// copy our position to lower level
			if (level) prev[level - 1] = prev[level];
			level--;
		}
		return prev;
	}
	
	add(key, value) {
		var me = new Node(key, value);
		// get all predecessors on all levels
		var prev = this.findPrevs(key);
		// get level number
		var level = this.randomlevel();
		for (var i = 0; i < level; i++) {
			var nx = prev[i].next[i];
			prev[i].next[i] = me;
			me.next[i] = nx;
		}
		return me;
	}
	
}