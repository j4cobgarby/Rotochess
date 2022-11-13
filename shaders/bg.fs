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
    //fragPos.xy += uTime/9.0;

    fragPos *= divisions;
    vec2 ipos = floor(fragPos);  // Get the integer coords
    vec2 fpos = fract(fragPos);  // Get the fractional coords

    float alpha = Rectangle(fpos, 2, 1.0);
    //vec3 color = vec3(fragPos.y, 1, 0);

    vec3 color = bott - topp;
    color = (color*((fragPos.y/4))) + topp;

    finalColor = vec4(color, 1);
}