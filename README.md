# 看看腿插件

<div style="text-align: center; margin: 20px 0;">
  <a href="https://github.com/ruin321/astrbot_plugin_leg_viewer" target="_blank" style="
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 15px 30px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 50px;
    text-decoration: none;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 600;
    font-size: 18px;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    transition: all 0.3s ease;
  " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(102, 126, 234, 0.4)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(102, 126, 234, 0.3)';">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
    </svg>
    <span>GitHub Stars</span>
    <img src="https://img.shields.io/github/stars/ruin321/astrbot_plugin_leg_viewer?style=flat&color=white&label=" alt="GitHub Stars">
  </a>
</div>

## 插件信息

- **名称**：看看腿插件
- **作者**：ruin311
- **版本**：1.0.0
- **描述**：呃呃呃 腿 好香😋😋😋
- **分类**：娱乐
- **项目地址**：https://github.com/ruin321/astrbot_plugin_leg_viewer

## 功能特性

- 随机获取神秘图片，刷出来什么看你自己，主要是凭运气

## 安装方法

1. 将插件目录 `astrbot_plugin_leg_viewer` 复制到 AstrBot 的 `data/plugins` 目录下
2. 重启 AstrBot 或在插件管理页面重载插件
3. 在插件管理页面启用插件

## 使用方法

### 命令列表

| 命令 | 描述 | 示例 |
|------|------|------|
| `/看看腿` | 随机获取腿部图片 | `/看看腿` |
| `/kkt` | 快捷命令，功能相同 | `/kkt` |
| `/看看腿 <分类ID>` | 获取指定分类的图片 | `/看看腿 101` |
| `/看看腿 list` | 查看可用分类列表 | `/看看腿 list` |

### 可用分类

- `101` - JKFUN-mobile
- `102` - 分类2
- `103` - 分类3
- `104` - 分类4

## 配置选项

在插件管理页面，可以修改以下配置：

| 配置项 | 描述 | 默认值 |
|--------|------|--------|
| 启用看看腿插件 | 是否启用插件 | true |
| 图床API密钥 | API访问密钥 | qq249663924 |
| 图床API地址 | API请求地址 | https://www.onexiaolaji.cn/RandomPicture/api |
| 默认分类ID | 默认使用的分类 | (空，随机分类) |
| 自定义分类ID列表 | 可用的分类列表 | 101\n102\n103\n104 |
| API请求超时时间 | 请求超时时间(秒) | 10 |

## API说明

- 使用的图床API：`https://www.onexiaolaji.cn/RandomPicture/api`
- API密钥：`qq249663924`

## 注意事项

1. 插件使用第三方图床API，需要网络连接才能正常工作
2. API可能会有时产出未经过审核的图片，请自行判断是否合适
3. api返回的图片可能会有nsfw内容，请自行判断是否合适
4. 插件默认只支持4个分类，如果需要更多分类，请在配置中添加
5. 本插件仅用于娱乐目的，看着图一乐即可

## 常见问题

### Q: 获取图片失败怎么办？
A: 请检查网络连接，或稍后重试。如果问题持续，请检查插件配置是否正确。

### Q: 可以添加更多分类吗？
A: 可以在配置中的"自定义分类ID列表"中添加更多分类ID。

## 更新日志

### v1.0.0
我不知道啊 自己看更新了啥


## 许可证

MIT License
