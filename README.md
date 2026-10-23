# ONWILO · 由行

**按自己的节奏，去喜欢的地方。**

ONWILO 是面向个人运动与探索的项目，计划逐步涵盖路线规划、训练管理、跑步与骑行记录、旅行安排、实时轨迹和数据分析。

仓库名：**on-will-oh**。当前已完成品牌图标资源初始化；应用功能尚未在此仓库实现。

| 浅色图标 | 深色图标 |
| :---: | :---: |
| <img src="public/brand/light/onwilo-256.png" width="200" height="200" alt="ONWILO 浅色图标：越野跑者沿砂石山径前往雪山"> | <img src="public/brand/dark/onwilo-256.png" width="200" height="200" alt="ONWILO 深色图标：越野跑者沿砂石山径前往雪山"> |

## 图标资源

图标采用已确认的第六版：双杖跑者、单色鞋形、砂石山径与有雪线层次的远山。原始 PNG 完整保留，前端文件通过尺寸与格式导出生成。

| 路径 | 用途 |
| --- | --- |
| assets/brand/original/onwilo-light.png | 浅色原始 PNG，1254 × 1254 |
| assets/brand/original/onwilo-dark.png | 深色原始 PNG，1254 × 1254 |
| public/brand/light/ | 浅色主题的 PNG、ICO、maskable 图标 |
| public/brand/dark/ | 深色主题的 PNG、ICO、maskable 图标 |
| public/favicon.ico | 默认 favicon，内含 16 / 32 / 48 px |
| public/apple-touch-icon.png | 默认 Apple Touch Icon，180 px |
| public/site.webmanifest | 浅色图标的 PWA manifest 模板 |
| public/site-dark.webmanifest | 深色图标的 PWA manifest 模板 |
| public/brand/brand.json | 品牌名称及各尺寸图标的 URL 清单 |
| examples/brand-preview.html | 实际尺寸与浅深色主题预览 |

每个主题提供 **16、32、48、64、128、180、192、256、512、1024 px** 方形 PNG。

普通图标保留完整方形底图，适用于网页、导航栏和头像位。专用 maskable 图标提供 192 / 512 px，给系统裁切预留了空间。当前交付格式为 PNG / ICO，原稿为栅格图片。

## 前端接入

将本仓库 public 目录中的内容复制到应用的 public 目录，保留目录结构。以下路径按站点根目录部署编写；使用子路径部署时，请加上应用自己的 base path。

### 网页头部

~~~html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32"
      href="/brand/light/onwilo-32.png" media="(prefers-color-scheme: light)">
<link rel="icon" type="image/png" sizes="32x32"
      href="/brand/dark/onwilo-32.png" media="(prefers-color-scheme: dark)">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
~~~

manifest 是可复用的应用配置模板；将来接入实际应用时，按应用的部署路径确认 id、start_url 和 scope。当前仓库没有实现离线缓存或安装后的应用页面。

### 浅深色自动切换

~~~html
<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="/brand/dark/onwilo-128.png">
  <img src="/brand/light/onwilo-128.png"
       width="64" height="64" alt="ONWILO · 由行">
</picture>
~~~

### React

~~~jsx
export function OnwiloIcon({ size = 48 }) {
  return (
    <picture>
      <source
        media="(prefers-color-scheme: dark)"
        srcSet="/brand/dark/onwilo-128.png"
      />
      <img
        src="/brand/light/onwilo-128.png"
        width={size}
        height={size}
        alt="ONWILO · 由行"
      />
    </picture>
  );
}
~~~

## 本地预览

在仓库根目录运行：

~~~sh
python3 -m http.server 8000 --bind 127.0.0.1
~~~

然后打开 http://127.0.0.1:8000/examples/brand-preview.html 。

## 重新导出

需要 Python 3.10 或更新版本。

~~~sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-assets.txt
python3 scripts/export_icons.py
~~~

导出脚本只负责缩放、格式转换和 maskable 留白，不重新设计图案。原始素材路径固定在 assets/brand/original/，生成文件可以直接提交到 Git。
