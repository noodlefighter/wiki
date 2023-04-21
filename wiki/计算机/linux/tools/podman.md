## 尝试用podman代替docker

因为podman没有deamon，如果目标是无痛替换，无需rootless模式，就需要直接在root下使用podman，run的时候记得使用`--privileged`，就基本能直接代替docker容器。

