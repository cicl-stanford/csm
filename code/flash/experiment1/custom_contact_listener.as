package {
	import Box2D.Collision.*;
	import Box2D.Collision.Shapes.*;
	import Box2D.Common.*;
	import Box2D.Common.Math.*;
	import Box2D.Dynamics.*;
	import Box2D.Dynamics.Contacts.*;
	import Box2D.Dynamics.Joints.*;

	//mean between position at BeginContact and EndContact can be used as contact point (taking the radius of the circle into account)
	
	class custom_contact_listener extends b2ContactListener {
		var collisionABStart:int = 0;
		var collisionWallStartA:int = 0;
		var collisionWallStartB:int = 0;
		
		override public function BeginContact(contact:b2Contact):void {
			// getting the fixtures that collided
			var fixtureA:b2Fixture=contact.GetFixtureA();
			var fixtureB:b2Fixture=contact.GetFixtureB();
			
			//contact between balls 
			if ((fixtureA.GetBody().GetUserData() == 'redBall' && fixtureB.GetBody().GetUserData() == 'greyBall') ||
				(fixtureA.GetBody().GetUserData() == 'greyBall' && fixtureB.GetBody().GetUserData() == 'redBall')){
				collisionABStart = 1;
			}

			//contact between grey ball and wall 
			if ((fixtureA.GetBody().GetUserData() == 'greyBall' && fixtureB.GetBody().GetUserData() == 'topWall')||
				(fixtureB.GetBody().GetUserData() == 'greyBall' && fixtureA.GetBody().GetUserData() == 'topWall')){ 				
				collisionWallStartA = 1;
			}

			if ((fixtureA.GetBody().GetUserData() == 'greyBall' && fixtureB.GetBody().GetUserData() == 'bottomWall')||
				(fixtureB.GetBody().GetUserData() == 'greyBall' && fixtureA.GetBody().GetUserData() == 'bottomWall')){ 				
				collisionWallStartA = 1;
			}

			if ((fixtureA.GetBody().GetUserData() == 'greyBall' && fixtureB.GetBody().GetUserData() == 'topLeftWall')||
				(fixtureB.GetBody().GetUserData() == 'greyBall' && fixtureA.GetBody().GetUserData() == 'topLeftWall')){ 				
				collisionWallStartA = 1;
			}

			if ((fixtureA.GetBody().GetUserData() == 'greyBall' && fixtureB.GetBody().GetUserData() == 'bottomLeftWall')||
				(fixtureB.GetBody().GetUserData() == 'greyBall' && fixtureA.GetBody().GetUserData() == 'bottomLeftWall')){ 				
				collisionWallStartA = 1;
			}

			//contact between red ball and wall 
			if ((fixtureA.GetBody().GetUserData() == 'redBall' && fixtureB.GetBody().GetUserData() == 'topWall')||
				(fixtureB.GetBody().GetUserData() == 'redBall' && fixtureA.GetBody().GetUserData() == 'topWall')){ 				
				collisionWallStartB = 1;
			}

			if ((fixtureA.GetBody().GetUserData() == 'redBall' && fixtureB.GetBody().GetUserData() == 'bottomWall')||
				(fixtureB.GetBody().GetUserData() == 'redBall' && fixtureA.GetBody().GetUserData() == 'bottomWall')){ 				
				collisionWallStartB = 1;
			}

			if ((fixtureA.GetBody().GetUserData() == 'redBall' && fixtureB.GetBody().GetUserData() == 'topLeftWall')||
				(fixtureB.GetBody().GetUserData() == 'redBall' && fixtureA.GetBody().GetUserData() == 'topLeftWall')){ 				
				collisionWallStartB = 1;
			}

			if ((fixtureA.GetBody().GetUserData() == 'redBall' && fixtureB.GetBody().GetUserData() == 'bottomLeftWall')||
				(fixtureB.GetBody().GetUserData() == 'redBall' && fixtureA.GetBody().GetUserData() == 'bottomLeftWall')){ 				
				collisionWallStartB = 1;
			}

		}
		override public function EndContact(contact:b2Contact):void {

		}
		
		//getter functions 
		public function getCollisionABStart():int{
			return collisionABStart;
		}
		public function getCollisionWallStartA():int{
			return collisionWallStartA;
		}
		public function getCollisionWallStartB():int{
			return collisionWallStartB;
		}

		//setter functions 
		public function setCollisionABStart():int{
			collisionABStart = 0;
			return collisionABStart;
		}
		public function setCollisionWallStartA():int{
			collisionWallStartA = 0;
			return collisionWallStartA;
		}
		public function setCollisionWallStartB():int{
			collisionWallStartB = 0;
			return collisionWallStartB;
		}
	}
}
