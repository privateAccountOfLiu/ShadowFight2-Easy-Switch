from __future__ import annotations

from typing import Dict

from python.util.settings import AppSettings


_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        # 应用基础
        "app.title": "Shadow Fight 2 Easy Switch",

        # 顶部菜单
        "menu.file": "File",
        "menu.export": "Export",
        "menu.setting": "Setting",
        "menu.help": "Help",
        "menu.help.about": "About",
        "menu.setting.settings": "Settings...",

        # 设置对话框
        "settings.title": "Settings",
        "settings.export.model": "Model export directory:",
        "settings.export.animation": "Animation export directory:",
        "settings.language": "Language:",
        "settings.language.en": "English",
        "settings.language.zh": "Simplified Chinese",
        "settings.restart.info": "Language changes will fully apply after restarting the application.",

        # 通用对话框
        "dialog.error.title": "Error",
        "dialog.notice.title": "Notice",
        "dialog.notice.default": "[Notice]: Transform Successfully!",
        "dialog.notice.no_file": "You Haven't Chose A File!",

        # About / 帮助窗口
        "about.title": "About Shadow Fight 2 Easy Switch",
        "about.author.label": "Author:",
        "about.version.label": "Version:",
        "about.github.label": "GitHub:",
        "about.github.link": "GitHub Repository",
        "about.license.text": (
            "This software is an open-source project based on PySide6. "
            "Use and distribution must comply with the applicable open-source license. "
            "All final rights of interpretation are reserved by the author, PrivateLiu."
        ),
        "about.close": "Close",

        # 主工具窗口按钮
        "main.button.model": "Model Editor",
        "main.button.csv": "Frames(.obj(multiple)) to (Format Data).csv",
        "main.button.animation": "Animation Editor",

        # 模型编辑器标签
        "label.range_x": "range(x):",
        "label.range_y": "range(y):",
        "label.range_z": "range(z):",
        "label.is_zoom": "is zoom:",
        "label.begin_id": "begin_id",
        "label.type": "type:",
        "label.rotate": "rotate:",
        "label.advanced_setting": "Advanced Setting",
        "button.apply": "Apply",

        # CSV 工具页
        "csv.window.title": "ToCsv",
        "csv.button.select_dir": "Select Dir",
        "csv.label.progress": "Progress:",
        "csv.label.title": (
            "<html><head/><body><p>"
            "<span style=\" font-size:12pt; font-weight:700;\">"
            "Bin: .objs to .csv"
            "</span></p>"
            "<p>output and input are in './objs_to_bin'</p>"
            "</body></html>"
        ),

        # 动画播放器按钮
        "anim.button.play": "Play",
        "anim.button.stop": "Stop",
        "anim.button.prev": "Last",
        "anim.button.next": "Next",
        "anim.button.reset_camera": "Reset Camera",
        "anim.checkbox.show_orbit": "Show Orbit",
        "anim.label.frame_prefix": "Frame:",
    },
    "zh-CN": {
        # 应用基础
        "app.title": "暗影格斗2 简易转换器",

        # 顶部菜单
        "menu.file": "文件",
        "menu.export": "导出",
        "menu.setting": "设置",
        "menu.help": "帮助",
        "menu.help.about": "关于",
        "menu.setting.settings": "设置...",

        # 设置对话框
        "settings.title": "设置",
        "settings.export.model": "模型导出目录：",
        "settings.export.animation": "动画导出目录：",
        "settings.language": "语言：",
        "settings.language.en": "英文",
        "settings.language.zh": "简体中文",
        "settings.restart.info": "语言变更将在应用重启后完全生效。",

        # 通用对话框
        "dialog.error.title": "错误",
        "dialog.notice.title": "提示",
        "dialog.notice.default": "[提示]: 转换成功！",
        "dialog.notice.no_file": "你还没有选择文件！",

        # About / 帮助窗口
        "about.title": "关于 暗影格斗2 简易转换器",
        "about.author.label": "作者：",
        "about.version.label": "版本：",
        "about.github.label": "GitHub：",
        "about.github.link": "GitHub 仓库",
        "about.license.text": (
            "本软件是基于 PySide6 的开源项目，"
            "使用和分发需遵守适用的开源许可证。"
            "本软件的最终解释权归作者 PrivateLiu 所有。"
        ),
        "about.close": "关闭",

        # 主工具窗口按钮
        "main.button.model": "模型编辑器",
        "main.button.csv": "帧(.obj 多个) 转 格式化数据 .csv",
        "main.button.animation": "动画编辑器",

        # 模型编辑器标签
        "label.range_x": "X 范围：",
        "label.range_y": "Y 范围：",
        "label.range_z": "Z 范围：",
        "label.is_zoom": "是否缩放：",
        "label.begin_id": "起始编号",
        "label.type": "类型：",
        "label.rotate": "旋转：",
        "label.advanced_setting": "高级设置",
        "button.apply": "应用",

        # CSV 工具页
        "csv.window.title": "批量导出 CSV",
        "csv.button.select_dir": "选择目录",
        "csv.label.progress": "进度：",
        "csv.label.title": (
            "<html><head/><body><p>"
            "<span style=\" font-size:12pt; font-weight:700;\">"
            "Bin：.objs 转 .csv"
            "</span></p>"
            "<p>输入与输出目录为 './objs_to_bin'</p>"
            "</body></html>"
        ),

        # 动画播放器按钮
        "anim.button.play": "播放",
        "anim.button.stop": "停止",
        "anim.button.prev": "上一帧",
        "anim.button.next": "下一帧",
        "anim.button.reset_camera": "重置相机",
        "anim.checkbox.show_orbit": "显示轨迹",
        "anim.label.frame_prefix": "帧：",
    },
}


def tr(key: str) -> str:
    """Translate a key according to current language in AppSettings."""
    lang = AppSettings.instance().language
    lang_map = _TRANSLATIONS.get(lang) or _TRANSLATIONS["en"]
    if key in lang_map:
        return lang_map[key]
    return _TRANSLATIONS["en"].get(key, key)

