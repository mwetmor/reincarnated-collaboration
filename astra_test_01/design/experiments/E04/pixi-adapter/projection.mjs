export function makeProjection(c){const t=c.elevation_deg*Math.PI/180,y=c.yaw_deg*Math.PI/180,f=202.5/Math.tan(c.vertical_fov_deg*Math.PI/360),st=Math.sin(t),ct=Math.cos(t),sy=Math.sin(y),cy=Math.cos(y),k=4/3;
 const project=(w,h=0)=>{const u=w[0],v=w[1],d=sy*u+cy*v,s=f/(c.distance_m-ct*d-st*h);return[(c.anchor[0]+s*(cy*u-sy*v))*k,(c.anchor[1]+s*(st*d-ct*h))*k];};
 const inverse=p=>{const x=p[0]/k-c.anchor[0],z=p[1]/k-c.anchor[1];const d=z*c.distance_m/(f*st+z*ct),r=x*(c.distance_m-ct*d)/f;return[cy*r+sy*d,-sy*r+cy*d];};return{project,inverse};}
