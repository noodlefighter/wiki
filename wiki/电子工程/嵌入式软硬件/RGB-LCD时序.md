# RGB LCD时序

> refers:
>
> - https://blog.csdn.net/qq_34509507/article/details/90406105
> - https://elixir.bootlin.com/linux/v4.3/source/Documentation/devicetree/bindings/video/display-timing.txt
> - 时序计算器：https://tomverbeure.github.io/video_timings_calculator

截取Linux设备树文档里的说明：

```
  +----------+-------------------------------------+----------+-------+
  |          |        ↑                            |          |       |
  |          |        |vback_porch                 |          |       |
  |          |        ↓                            |          |       |
  +----------#######################################----------+-------+
  |          #        ↑                            #          |       |
  |          #        |                            #          |       |
  |  hback   #        |                            #  hfront  | hsync |
  |   porch  #        |       hactive              #  porch   |  len  |
  |<-------->#<-------+--------------------------->#<-------->|<----->|
  |          #        |                            #          |       |
  |          #        |vactive                     #          |       |
  |          #        |                            #          |       |
  |          #        ↓                            #          |       |
  +----------#######################################----------+-------+
  |          |        ↑                            |          |       |
  |          |        |vfront_porch                |          |       |
  |          |        ↓                            |          |       |
  +----------+-------------------------------------+----------+-------+
  |          |        ↑                            |          |       |
  |          |        |vsync_len                   |          |       |
  |          |        ↓                            |          |       |
  +----------+-------------------------------------+----------+-------+

Example:

	display-timings {
		native-mode = <&timing0>;
		timing0: 1080p24 {
			/* 1920x1080p24 */
			clock-frequency = <52000000>;
			hactive = <1920>;
			vactive = <1080>;
			hfront-porch = <25>;
			hback-porch = <25>;
			hsync-len = <25>;
			vback-porch = <2>;
			vfront-porch = <2>;
			vsync-len = <2>;
			hsync-active = <1>;
		};
	};
```