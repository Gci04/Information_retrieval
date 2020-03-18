function probf(n, m) {
	return function(k) {
		return Math.pow(1 - Math.exp(-k*n/m), k);
	}
}

/* https://habrahabr.ru/post/112069/ */
function hashbuilder() {
    var seed = Math.floor(Math.random() * 32) + 32;
    return function (str) {
		var result = 1;
		for (var i = 0; i < str.length; ++i)
			result = (seed * result + str.charCodeAt(i)) & 0xFFFFFFFF;
		return result;
    };
}

class Bits {
	constructor(L) { this.bits = []; this.bits.length = parseInt(L / 32) + 1;  }
	test(index) { return (this.bits[Math.floor(index / 32)] >>> (index % 32)) & 1; }
	set(index) { this.bits[Math.floor(index / 32)] |= 1 << (index % 32); }
}

class BloomSet {
	static getParams(maxItems, error_probability) {
		var size = -(maxItems * Math.log(error_probability)) / (Math.LN2 * Math.LN2);
		var count = (size / maxItems) * Math.LN2;
		size = Math.round(size);
		count = Math.round(count);
		return { size: size, fncount: count};
	}

	constructor(size, functionCount) {
		this.size = size;
		this.bits = new Bits(size);
		this.functions = [];
		for (var i = 0; i < functionCount; i++)
			this.functions.push(hashbuilder());
	}

	add(str) {
		for (var i in this.functions) {
			var x = (this.functions[i](str)) % this.size;
			this.bits.set(x);
		}
	}
    
	test(string) {
		for (var i in this.functions)
			if (!this.bits.test(this.functions[i](string) % this.size)) return false;
		return true;
	}
}