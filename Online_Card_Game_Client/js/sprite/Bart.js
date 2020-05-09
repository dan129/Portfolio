class Bart{
	constructor(){
		this.x = 0;
		this.y = 120;
		let columnCount = 12;
		let rowCount = 3;
		let refreshDelay = 100;
		let scale = 2;
		let rowLoop = true
		this.tiledImage = new TiledImage("sprite/bartSkate.png",
										columnCount,rowCount,refreshDelay,
										rowLoop,scale);

		this.tiledImage.setFlipped(true)

		this.tiledImage.setFullImageLoop(24)
	}
	tick () {
        this.x+=3;
		this.tiledImage.tick(this.x, this.y, ctx);

		//tant que bart ne depasse pas la longueur de la fenetre
		if(this.x <= window.innerWidth){
			return true;
		}
		else{
			return false;
		}
	}
}