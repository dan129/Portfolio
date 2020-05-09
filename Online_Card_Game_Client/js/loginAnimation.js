let ctx = null;
let spriteList = [];
let img = new Image();

window.addEventListener("load", ()=>{
	ctx = document.querySelector("#canvas").getContext("2d");
	document.querySelector("#canvas").width = window.innerWidth;
	document.querySelector("#canvas").height = "220";
	spriteList.push(new Bart());
	tick();
})

const tick =() =>{
	ctx.clearRect(0, 0, window.innerWidth, 220);
	for (let i = 0; i < spriteList.length; i++) {
		let alive = spriteList[i].tick();

		if (!alive) {
			spriteList.splice(i, 1);
			i--;
		}
	}

	window.requestAnimationFrame(tick);
}