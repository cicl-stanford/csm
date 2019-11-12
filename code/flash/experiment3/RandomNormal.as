package{
	import flash.display.Sprite;

	public class RandomNormal extends Sprite
	{
		/**
		 *	Returns a Number ~ N(0,1);
		 */
		private var ready : Boolean;
		private var cache : Number;
		public function standardNormal () : Number
		{
			if ( ready )
			{				//  Return a cached result
				ready = false;		//  from a previous call
				return cache;		//  if available.
			}
			
			var	x : Number,		//  Repeat extracting uniform values
			y : Number,		//  in the range ( -1,1 ) until
			w : Number;		//  0 < w = x*x + y*y < 1
			do
			{
				x = 2* Math.random() - 1;
				y = 2* Math.random() - 1;
				w = x * x + y * y;
			}
			while ( w >= 1 || !w );
			
			w = Math.sqrt ( -2 * Math.log ( w ) / w );
			
			ready = true;
			cache = x * w;			//  Cache one of the outputs
			return y * w;			//  and return the other.
		}
	}	
}