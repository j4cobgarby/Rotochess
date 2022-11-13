#version 330

// Input vertex attributes (from vertex shader)
in vec3 fragPosition;
in vec2 fragTexCoord;
//in vec4 fragColor;
in vec3 fragNormal;

// Input uniform values
uniform sampler2D texture0;
uniform vec4 colDiffuse;

// Output fragment color
out vec4 finalColor;


// Input lighting values
uniform vec4 ambient;
uniform vec3 viewPos;

void main()
{
    // Gamma correction
    finalColor = colDiffuse*clamp(dot(vec3(1,1,0),fragNormal),0.4,1);//pow(finalColor, vec4(1.0/2.2));
    finalColor.w = 1;
}