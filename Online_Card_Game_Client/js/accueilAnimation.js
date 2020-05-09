let ctx = null;
let img = new Image();
window.addEventListener("load", ()=>{
	let width = 120;
	let height = 100;
	/*ctx = document.querySelector("#canvas").getContext("2d");
	document.querySelector("#canvas").width = width;
	document.querySelector("#canvas").height = height;
	/*img.src = "images/maison.png"*/
	/*let gif = new GIF();
 	gif.src = ("../images/monkey.gif");*/
/*
	img.src = './images/monkey.gif';
	ctx.fillStyle = "#FF0000";
	ctx.drawImage(img,0,0);
	//ctx.fillRect(0, 0, width, height);

*/
	//tick();
})

const tick =() =>{
	ctx.drawImage(img,0,0);

	window.requestAnimationFrame(tick);
}