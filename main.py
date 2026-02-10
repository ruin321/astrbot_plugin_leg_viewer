from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api import AstrBotConfig
import httpx
import json

@register("astrbot_plugin_leg_viewer", "ruin311", "这看看腿 多是一件美事啊😋😋😋", "1.0.0", "https://github.com/ruin321/astrbot_plugin_leg_viewer")
class LegViewerPlugin(Star):
    """
    看看腿插件

    这看看腿 多是一件美事啊😋😋😋
    """
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        
        # 加载配置
        self.enabled = self.config.get("enabled", True)
        self.api_key = self.config.get("api_key", "qq249663924")
        self.api_url = self.config.get("api_url", "https://www.onexiaolaji.cn/RandomPicture/api")
        self.default_class = self.config.get("default_class", "")
        self.custom_classes = self.config.get("custom_classes", "101\n102\n103\n104")
        self.timeout = self.config.get("timeout", 10)
        
        # 解析自定义分类列表
        self.class_list = []
        if self.custom_classes:
            self.class_list = [cls.strip() for cls in self.custom_classes.split('\n') if cls.strip()]
        
        logger.info(f"看看腿插件已加载。启用状态: {self.enabled}, 作者: ruin311")
    
    async def get_leg_image(self, class_id: str = ""):
        """调用图床API获取腿部图片"""
        try:
            logger.info(f"开始获取腿部图片，分类ID: {class_id or self.default_class or '随机'}")
            
            # 直接使用示例格式构建URL
            api_url = "https://www.onexiaolaji.cn/RandomPicture/api/"
            
            # 构建查询参数
            params = {
                "key": self.api_key,
                "type": "json"
            }
            
            # 如果指定了分类，则添加分类参数
            if class_id or self.default_class:
                params["class"] = class_id or self.default_class
            
            # 构建完整URL
            import urllib.parse
            query_string = urllib.parse.urlencode(params)
            full_url = f"{api_url}?{query_string}"
            logger.info(f"请求URL: {full_url}")
            
            # 发送API请求
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"发送API请求...")
                response = await client.get(full_url)
                response.raise_for_status()
                
                # 打印原始响应
                raw_response = response.text
                logger.info(f"API响应状态码: {response.status_code}")
                logger.info(f"原始响应: {raw_response}")
                
                # 解析响应
                try:
                    data = response.json()
                    logger.info(f"解析后的响应: {data}")
                    
                    # 检查响应格式
                    if isinstance(data, dict):
                        # 检查URL字段是否存在
                        if "url" in data:
                            image_url = data["url"]
                            logger.info(f"获取图片成功，分类: {data.get('class', '未知')}，URL: {image_url}")
                            return image_url
                        # 检查其他可能的字段
                        elif "image" in data and isinstance(data["image"], dict) and "url" in data["image"]:
                            image_url = data["image"]["url"]
                            logger.info(f"获取图片成功，URL: {image_url}")
                            return image_url
                        # 检查code字段
                        elif "code" in data:
                            logger.info(f"API返回状态码: {data['code']}")
                            # 即使code不是200，也要检查是否有url字段
                            if "url" in data:
                                image_url = data["url"]
                                logger.info(f"获取图片成功（非标准状态码），URL: {image_url}")
                                return image_url
                except json.JSONDecodeError as e:
                    logger.error(f"JSON解析失败: {e}")
                    # 如果不是JSON，尝试直接返回响应内容
                    if raw_response.startswith("http"):
                        logger.info(f"直接返回非JSON响应作为URL: {raw_response}")
                        return raw_response
                
                logger.error(f"无法从响应中提取URL: {raw_response[:200]}")
                return None
                
        except httpx.RequestError as e:
            logger.error(f"API请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"API响应解析失败: {e}")
            return None
        except Exception as e:
            logger.error(f"获取图片失败: {e}")
            return None
    
    @filter.command("看看腿", alias={"kkt"})
    async def leg_viewer(self, event: AstrMessageEvent, class_id: str = ""):
        """看看腿命令
        Args:
            class_id: 可选，指定分类ID
        """
        # 检查插件是否启用
        if not self.enabled:
            yield event.plain_result("插件已禁用，请在配置中启用")
            return
        
        # 如果用户输入的是 "list"，显示可用分类
        if class_id.lower() == "list":
            async for result in self.show_classes(event):
                yield result
            return
        
        # 发送加载中提示
        await event.send(event.plain_result("正在获取图片..."))
        
        # 调用API获取图片
        image_url = await self.get_leg_image(class_id)
        
        if image_url:
            # 发送图片
            yield event.image_result(image_url)
        else:
            # 发送错误提示
            yield event.plain_result("获取图片失败，请稍后再试")
    
    async def show_classes(self, event: AstrMessageEvent):
        """显示可用的分类列表"""
        if not self.class_list:
            yield event.plain_result("暂无可用分类，请在配置中添加")
            return
        
        # 构建分类列表
        class_list_str = "\n".join([f"- {cls}" for cls in self.class_list])
        response = f"📋 可用分类列表：\n{class_list_str}\n\n使用方法：/看看腿 <分类ID>"
        
        yield event.plain_result(response)
    

    
    async def terminate(self):
        """插件卸载时调用"""
        logger.info("看看腿插件已卸载")