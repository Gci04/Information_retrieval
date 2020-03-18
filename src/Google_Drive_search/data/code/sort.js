// A function to do counting sort of arr[] according to
// the digit represented by exp.
function countSort(arr, base, exp) {
	var output = []; output.length = arr.length;
	var count = [];  count.length = base;
	for (var i = 0; i < arr.length; i++)
        	count[(arr[i]/exp)%base]++;
	// Change count[i] so that count[i] now contains actual
	//  position of this digit in output[]
	for (i = 1; i < base; i++)
        	count[i] += count[i - 1];
	 // Build the output array
	for (i = arr.length - 1; i >= 0; i--) {
		output[count[ (arr[i]/exp)%base ] - 1] = arr[i];
		count[ (arr[i]/exp)%base ]--;
	}
	return arr; 
}
 
function radixsort(arr) {
	var base = 2;
	var max = Math.pow(base, 32);
	for (var exp = 1; max/exp > 1; exp *= base) {
		arr = countSort(arr, base, exp);
	}
}

/* http://www.stoimen.com/blog/2010/07/09/friday-algorithms-javascript-bubble-sort/ */
function bubblesort(a) {
    var swapped;
    do {
        swapped = false;
        for (var i=0; i < a.length-1; i++) {
            if (a[i] > a[i+1]) {
                var temp = a[i];
                a[i] = a[i+1];
                a[i+1] = temp;
                swapped = true;
            }
        }
    } while (swapped);
}