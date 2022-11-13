#version 330

// Input vertex attributes (from vertex shader)
in vec2 fragTexCoord;
in vec4 fragColor;

// Output fragment color
out vec4 finalColor;

// Custom variables
#define PI 3.14159265358979323846
uniform float uTime = 0.0;

float divisions = 5.0;
float angle = 0.0;

vec3 bott = vec3(0.087,0.168,0.239);
vec3 topp = vec3(0.231,0.567,0.886);

float Rectangle(in vec2 st, in float size, in float fill)
{
  float roundSize = 0.5 - size/2.0;
  float left = step(roundSize, st.x);
  float top = step(roundSize, st.y);
  float bottom = step(roundSize, 1.0 - st.y);
  float right = step(roundSize, 1.0 - st.x);

  return (left*bottom*right*top)*fill;
}

void main()
{
  vec2 fragPos = fragTexCoord;

	vec2 uv = 2.0*fragTexCoord.xy;

    // background	 
	vec3 color = vec3(0.3 + 0.2*uv.y);

    // bubbles	
	for( int i=0; i<40; i++ )
	{
        // bubble seeds
		float pha =      sin(float(i)*546.13+1.0)*0.5 + 0.5;
		float siz = pow( sin(float(i)*651.74+5.0)*0.5 + 0.5, 4.0 );
		float pox =      sin(float(i)*321.55+4.1);

        // buble size, position and color
		float rad = 0.1 + 0.5*siz;
		vec2  pos = vec2( pox, -rad + (2.0+2.0*rad)*mod(pha+0.1*uTime*(0.2+0.8*siz),1.0));
    pos = pos * vec2(1,-1);
    pos = pos + vec2(0,1);
		float dis = length( uv - pos );
		vec3  col = mix( vec3(0.0,0.0,0.0), vec3(0.1,0.4,0.8), 0.5+0.5*sin(float(i)*1.2+1.9));
		//    col+= 8.0*smoothstep( rad*0.95, rad, dis );
		
        // render
		float f = length(uv-pos)/rad;
		f = sqrt(clamp(1.0-f*f,0.0,0.5));
		color -= col.zyx *(1.0-smoothstep( rad*0.95, rad, dis )) * f;
	}

    // vigneting	
	color *= sqrt(1.5-0.2*length(uv));

  vec3 colour = bott - topp;
  colour = (colour*((fragPos.y/4))) + topp;

  color = color*0.3+colour;

	finalColor = vec4(color,1.0);
}