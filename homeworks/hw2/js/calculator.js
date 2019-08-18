var queue = [];
var coeff = 10;

function clickNum(num) {
	var dispEl = document.getElementById("calc-display");
	var dispStr = dispEl.value;
	var disp = parseInt(dispStr);

	dispEl.value = coeff*disp + num;
	coeff = 10;
}

function clickOps(op) {
	var dispEl = document.getElementById("calc-display");
	var dispStr = dispEl.value;
	coeff = 0;

	console.log("Current display: " + dispStr);
	console.log("Ops key entered: " + op);
	queue.push(dispStr);
	queue.push(op);

	var val1, prevOp, val2, ans = null;
	if (queue.length >= 3) {
		val1 = parseInt(queue.shift());
		prevOp = queue.shift();
		val2 = parseInt(queue.shift());

		switch(prevOp) {
			case '+':
				ans = val1+val2;
				break;
			case '-':
				ans = val1-val2;
				break;
			case '*':
				ans = val1*val2;
				break;
			case '/':
				ans = parseInt(val1/val2);
				if (isNaN(ans)) {
					ans = 0;
					alert("Dividing by zero!");
				}
				break;
			default:
				ans = parseInt(dispStr);
		}

		dispEl.value = ans;
		queue.unshift(ans.toString());
	}	
}