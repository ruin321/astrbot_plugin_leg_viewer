from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api import AstrBotConfig
import httpx
import json
import urllib.parse

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
    
    def _is_valid_url(self, url):
        """验证URL是否有效"""
        if not url:
            return False
        url = url.strip()
        return url.startswith("http://") or url.startswith("https://")
    
    async def get_leg_image(self, class_id: str = ""):
        """调用图床API获取腿部图片"""
        try:
            logger.debug(f"开始获取腿部图片，分类ID: {class_id or self.default_class or '随机'}")
            
            # 使用配置的API URL
            api_url = self.api_url.rstrip("/") + "/"
            
            # 构建查询参数
            params = {
                "type": "json"
            }
            
            # 如果指定了分类，则添加分类参数
            if class_id or self.default_class:
                params["class"] = class_id or self.default_class
            
            # 构建完整URL（不记录key）
            safe_params = params.copy()
            if self.api_key:
                safe_params["key"] = "***"
            
            # 记录安全的URL（不包含key）
            safe_url = api_url + "?" + urllib.parse.urlencode(safe_params)
            logger.debug(f"请求URL: {safe_url}")
            
            # 添加key参数（不记录到日志）
            params["key"] = self.api_key
            
            # 发送API请求
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.debug(f"发送API请求...")
                response = await client.get(api_url, params=params)
                response.raise_for_status()
                
                # 解析响应
                raw_response = response.text.strip()
                logger.debug(f"API响应状态码: {response.status_code}")
                
                try:
                    data = response.json()
                    logger.debug(f"解析后的响应: {data}")
                    
                    # 检查响应格式
                    if isinstance(data, dict):
                        # 直接返回URL
                        if "url" in data:
                            image_url = data["url"]
                            if self._is_valid_url(image_url):
                                logger.info(f"获取图片成功，分类: {data.get('class', '未知')}")
                                return image_url
                            else:
                                logger.error(f"无效的图片URL: {image_url}")
                                return None
                        # 检查其他可能的字段
                        elif "data" in data:
                            if isinstance(data["data"], dict) and "url" in data["data"]:
                                image_url = data["data"]["url"]
                                if self._is_valid_url(image_url):
                                    logger.info(f"获取图片成功")
                                    return image_url
                                else:
                                    logger.error(f"无效的图片URL: {image_url}")
                                    return None
                            elif isinstance(data["data"], str) and self._is_valid_url(data["data"]):
                                logger.info(f"获取图片成功")
                                return data["data"]
                except json.JSONDecodeError as e:
                    logger.debug(f"JSON解析失败: {e}")
                    # 如果不是JSON，尝试直接返回响应内容
                    if self._is_valid_url(raw_response):
                        logger.info(f"直接返回非JSON响应作为URL")
                        return raw_response
                
                logger.error(f"无法从响应中提取有效的URL")
                return None
                
        except httpx.RequestError as e:
            logger.error(f"API请求失败: {e}")
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