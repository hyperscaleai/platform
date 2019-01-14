# build image via Dockerfile
## base image
FROM nginx:1.11-alpine
## commands: run, copy
COPY index.html /user/share/nginx/html/index.html
## expose port
EXPOSE 80
## commands
With the Docker image configured and having defined which ports we want accessible, 
we now need to define the command that launches the application.

The CMD line in a Dockerfile defines the default command to run when a container is launched. 
If the command requires arguments then it's recommended to use an array, 
for example ["cmd", "-a", "arga value", "-b", "argb-value"], which will be combined together 
and the command cmd -a "arga value" -b argb-value would be run.

```
CMD ["nginx","-g","daemon off;"]

```

## Entry point
An alternative approach to CMD is ENTRYPOINT. While a CMD can be overridden when the container 
starts, a ENTRYPOINT defines a command which can have arguments passed to it when
 the container launches.
 
## build container
Using the docker build command to build the image. You can give the image a friendly name by using the -t <name> option.
```
docker build . -t img1:v1
```

## run image
```
docker run -d -p 80:80 img1:v1
```