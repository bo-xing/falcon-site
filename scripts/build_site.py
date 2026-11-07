#!/usr/bin/env python3
"""Build the dependency-free GitHub Pages site. Edit this file or content/*.html."""
from pathlib import Path
from html import escape
from datetime import date
import argparse
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://bo-xing.github.io/falcon-site/"
APPLE = "https://apps.apple.com/app/id6780008195"
PLAY = "https://play.google.com/store/apps/details?id=com.boxing.falcon"
EMAIL = "boxing.support@gmail.com"
UPDATED = "2026-11-07"


def updated_label(lang):
    """Use the same release date in visible copy and the sitemap, on every OS."""
    updated = date.fromisoformat(UPDATED)
    if lang == 'zh':
        return f'更新日期：{updated.year} 年 {updated.month} 月 {updated.day} 日'
    months = ('January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December')
    return f'Updated {months[updated.month - 1]} {updated.day}, {updated.year}'


def icon(name):
    paths = {
        "arrow": '<path d="M7 17 17 7M7 7h10v10"/>',
        "connect": '<path d="M8 12h8M5 8v8M19 8v8M2 10v4M22 10v4"/>',
        "listen": '<circle cx="12" cy="12" r="2"/><path d="M7 7a7 7 0 0 0 0 10M17 7a7 7 0 0 1 0 10M4 4a11 11 0 0 0 0 16M20 4a11 11 0 0 1 0 16"/>',
        "ssh": '<path d="m5 7 5 5-5 5M13 17h6"/>',
        "check": '<path d="m5 12 4 4L19 6"/>',
        "wifi": '<path d="M2 8a16 16 0 0 1 20 0M5 12a11 11 0 0 1 14 0M8 16a6 6 0 0 1 8 0"/><circle cx="12" cy="20" r=".7"/>',
        "server": '<rect x="4" y="3" width="16" height="7" rx="2"/><rect x="4" y="14" width="16" height="7" rx="2"/><path d="M8 6.5h.01M8 17.5h.01M12 6.5h4M12 17.5h4"/>',
        "chart": '<path d="M3 3v18h18M6 16l4-5 4 2 6-8"/>',
    }
    return f'<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def route(page, lang):
    return ("index" if page == "home" else page) + ("-zh" if lang == "zh" else "") + ".html"


def translate(lang):
    return lambda en, zh: zh if lang == "zh" else en


def store_links(lang):
    return f'''<div class="store-links">
      <a class="button store-button primary" href="{APPLE}"><span><small>iPhone · iPad · Mac</small>App Store</span>{icon('arrow')}</a>
      <a class="button store-button secondary" href="{PLAY}"><span><small>Android</small>Google Play</span>{icon('arrow')}</a>
    </div>'''


def header(page, lang):
    t = translate(lang)
    home = route('home', lang)
    other = 'en' if lang == 'zh' else 'zh'
    return f'''<a class="skip-link" href="#main-content">{t('Skip to content','跳至正文')}</a>
    <header class="site-header"><div class="container header-inner">
      <a class="brand" href="{home}" aria-label="{t('iPerf Falcon home','iPerf Falcon 首页')}"><img src="app-icon.png" width="38" height="38" alt=""><span>iPerf Falcon</span></a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav" hidden>{t('Menu','菜单')}<span aria-hidden="true">＋</span></button>
      <nav class="site-nav" id="main-nav" aria-label="{t('Primary navigation','主导航')}">
        <a href="{home}#features">{t('Features','功能')}</a><a href="{home}#use-cases">{t('Use cases','场景')}</a><a href="{home}#pro">Pro</a>
        <a href="{route('support',lang)}"{' aria-current="page"' if page == 'support' else ''}>{t('Support','支持')}</a>
        <a class="language-link" href="{route(page,other)}" lang="{'en' if other == 'en' else 'zh-Hans'}" hreflang="{'en' if other == 'en' else 'zh-Hans'}" aria-label="{t('切换至中文','Switch to English')}">{t('中文','EN')}</a>
        <button class="theme-toggle" type="button" data-dark-label="{t('Use dark appearance','使用深色外观')}" data-light-label="{t('Use light appearance','使用浅色外观')}" aria-label="{t('Change appearance','切换外观')}" hidden><span aria-hidden="true">◐</span></button>
        <a class="nav-download" href="{home}#download">{t('Get Falcon','下载 Falcon')}</a>
      </nav>
    </div></header>'''


def footer(lang):
    t = translate(lang)
    return f'''<footer class="site-footer"><div class="container footer-inner">
      <div><a class="brand footer-brand" href="{route('home',lang)}"><img src="app-icon.png" width="30" height="30" alt="">iPerf Falcon</a><p>{t('Your endpoints. Your measurements.','自己选择对端，掌握真实测量。')}</p><small>© 2026 Bo Xing</small></div>
      <nav class="footer-links" aria-label="{t('Footer navigation','页脚导航')}"><a href="{route('support',lang)}">{t('Support','技术支持')}</a><a href="{route('privacy',lang)}">{t('Privacy','隐私政策')}</a><a href="{route('terms',lang)}">{t('Terms','使用条款')}</a><a href="mailto:{EMAIL}">{t('Contact','联系我们')}</a></nav>
    </div></footer>'''


def shot(lang, platform, stage, caption, priority=False):
    t = translate(lang)
    src = f'assets/screenshots/{platform}-{lang}-{stage}.jpg'
    names = {'ios':'iOS','android':'Android','mac':'macOS'}
    return f'''<figure class="screenshot-card"><a class="screenshot-link" href="{src}" data-lightbox aria-label="{t('Enlarge: ','放大查看：')}{escape(names[platform]+' · '+caption)}"><img src="{src}" alt="{escape(names[platform]+' · '+caption)}" {'fetchpriority="high"' if priority else 'loading="lazy"'} decoding="async" width="{'1800' if platform=='mac' else '828' if platform=='ios' else '802'}" height="{'1266' if platform=='mac' else '1800'}"></a><figcaption><span>{caption}</span><span class="expand-hint" aria-hidden="true">↗</span></figcaption></figure>'''


def home(lang):
    t = translate(lang)
    support = route('support',lang)
    workflows = [
        ('connect',t('Connect','连接'),t('Choose your endpoint.','选择你要测的对端。'),t('Enter an iPerf host, reuse a saved target, or try an independent public server.','输入 iPerf 地址、复用常用目标，或选择第三方公共服务器。')),
        ('listen',t('Listen','监听'),t('Make your device the server.','让手边设备成为服务端。'),t('See the address to connect to, then accept client sessions until you stop listening.','清楚查看对端应连接的地址，持续接受客户端会话，直到你停止监听。')),
        ('ssh',t('Automate with SSH','SSH 编排'),t('Let Falcon handle the setup.','把启动与收尾交给 Falcon。'),t('Connect to OpenWrt or Linux, start the remote endpoint, run your test, and clean up. Requires Pro.','连接 OpenWrt 或 Linux，自动启动对端、执行测试并清理。需要 Pro。')),
    ]
    help_anchors = {'connect': 'quick-start', 'listen': 'listening', 'ssh': 'ssh'}
    workflow_html = ''.join(f'''<article class="workflow"><div class="workflow-top"><span class="icon-box">{icon(kind)}</span><span class="step-number">0{i}</span></div><h3>{title}</h3><p class="workflow-subtitle">{subtitle}</p><p>{text}</p><a class="text-link" href="{support}#{help_anchors[kind]}" aria-label="{t('How it works','查看使用方法')} · {title}">{t('How it works','查看使用方法')} <span aria-hidden="true">↗</span></a></article>''' for i,(kind,title,subtitle,text) in enumerate(workflows,1))
    panels = ''
    for platform in ['ios','android','mac']:
        shots = shot(lang,platform,'speed',t('Live throughput & protocol metrics','实时吞吐与协议指标'))
        if platform != 'mac':
            shots += shot(lang,platform,'ssh',t('SSH targets & orchestration','SSH 对端与远程编排'))
            shots += shot(lang,platform,'compare',t('Compare saved measurements','对比已保存的测量'))
        panels += f'''<section class="screenshot-panel" id="screens-{platform}" aria-labelledby="tab-{platform}"><h3 class="no-js-platform">{'iPhone / iPad' if platform=='ios' else 'Android' if platform=='android' else 'Mac'}</h3><div class="screens-grid{' wide-screen' if platform=='mac' else ''}">{shots}</div></section>'''
    cases = [
        ('wifi',t('Find the weak spot in your Wi-Fi.','找出 Wi-Fi 的薄弱位置。'),t('Keep the endpoint and test settings fixed. Measure in different rooms, then compare saved runs to see how throughput changes.','固定对端和测试参数，在不同房间测量，再对比历史记录，观察吞吐变化。'),t('Home networks · Wi-Fi coverage','家庭网络 · Wi-Fi 覆盖')),
        ('server',t('Check the path to your NAS.','看清通往 NAS 的链路表现。'),t('Test against an iPerf host on your LAN to investigate wired, wireless, router, or server bottlenecks.','在局域网中连接 iPerf 对端，排查有线、无线、路由器或服务器的吞吐瓶颈。'),t('LAN · Ethernet · NAS','局域网 · 有线网络 · NAS')),
        ('ssh',t('Spend less time setting up tests.','减少重复配置的时间。'),t('Use SSH orchestration, saved commands, and presets to repeat a measurement workflow on your own equipment.','用 SSH 编排、命令收藏和参数预设，在自己的设备上重复同一套测量流程。'),t('OpenWrt · Linux · Pro','OpenWrt · Linux · Pro')),
    ]
    cases_html = ''.join(f'<article class="use-case"><span class="icon-box">{icon(kind)}</span><div><p class="eyebrow">{label}</p><h3>{title}</h3><p>{text}</p></div></article>' for kind,title,text,label in cases)
    rows = [
        (t('Core TCP / UDP testing','基础 TCP／UDP 测试'),True,True),
        (t('Local server & live charts','本机服务端与实时曲线'),True,True),
        (t('History, individual exports & share cards','历史、单条导出与分享卡片'),True,True),
        (t('SSH orchestration & saved targets','SSH 编排与保存常用目标'),False,True),
        (t('Advanced parameters, commands & presets','高级参数、命令模式与预设'),False,True),
        (t('Multi-run comparison & batch export','多条结果对比与批量导出'),False,True),
    ]
    def cell(yes):
        return f'<span class="check">{icon("check")}<span class="sr-only">{t("Included","包含")}</span></span>' if yes else f'<span class="not-included" aria-label="{t("Not included","不包含")}">—</span>'
    rows_html = ''.join(f'<tr><th scope="row">{label}</th><td>{cell(free)}</td><td>{cell(pro)}</td></tr>' for label,free,pro in rows)
    faqs = [
        (t('Do I need an iPerf server?','测速需要 iPerf 服务端吗？'),t('Yes. Connect to a compatible iPerf host, make another device the server, choose a third-party public server, or use Pro SSH orchestration to start your own endpoint.','需要。你可以连接兼容的 iPerf 对端、让另一台设备监听、选择第三方公共服务器，或使用 Pro 的 SSH 编排启动自己的对端。')),
        (t('Is Pro a subscription?','Pro 是订阅吗？'),t('No. Pro is an optional one-time in-app purchase. Apple and Google Play purchases are separate; use the account from the original store to restore access.','不是。Pro 为可选的一次性应用内购买。Apple 与 Google Play 购买相互独立，恢复时请使用原商店的购买账号。')),
        (t('Where does my test data go?','测试数据会发送到哪里？'),t('Test traffic goes to your chosen endpoint. History stays on your device. Falcon has no account system, ads, or analytics. Store services and third-party endpoints follow their own policies.','测试流量发送到你选择的对端，历史记录保存在设备本地。Falcon 无需账号，不含广告或分析追踪；商店服务与第三方对端适用各自政策。')),
    ]
    faq_html = ''.join(f'<details class="faq-item"><summary>{q}</summary><div class="faq-answer"><p>{a}</p></div></details>' for q,a in faqs)
    return f'''<main id="main-content" tabindex="-1">
      <section class="hero container" aria-labelledby="hero-title">
        <div class="hero-copy"><p class="eyebrow"><span class="status-dot" aria-hidden="true"></span>{t('A native iPerf toolkit','原生 iPerf 网络测试工具')}</p>
          <h1 id="hero-title">{t('Your network.<br><span>In clear view.</span>','看清网络的<br><span>真实吞吐表现。</span>')}</h1>
          <p class="hero-description">{t('Measure Wi-Fi, LAN, and server throughput with iPerf3 and iPerf2. Choose your endpoints, see live results, and keep every useful measurement.','用 iPerf3 与 iPerf2 测量 Wi-Fi、局域网和服务器吞吐。自己选择对端，实时查看结果，留住每一次有价值的测量。')}</p>
          {store_links(lang)}<p class="download-note">{t('Free to download · Optional one-time Pro upgrade','免费下载 · Pro 可选一次性升级')}</p>
          <ul class="hero-facts"><li>{icon('check')}{t('No account','无需账号')}</li><li>{icon('check')}{t('No ads or analytics','无广告与分析追踪')}</li></ul>
        </div>
        <div class="hero-visual"><div class="visual-orbit" aria-hidden="true"></div>
          <div class="hero-phone hero-ios"><span class="device-label">iOS</span><a href="assets/screenshots/ios-{lang}-speed.jpg" data-lightbox aria-label="{t('Enlarge iOS test screen','放大 iOS 测速界面')}"><img src="assets/screenshots/ios-{lang}-speed.jpg" alt="{t('Falcon on iOS showing a live throughput test and chart','Falcon iOS 实时测速读数与曲线')}" width="828" height="1800" fetchpriority="high"></a></div>
          <div class="hero-phone hero-android"><span class="device-label">Android</span><a href="assets/screenshots/android-{lang}-speed.jpg" data-lightbox aria-label="{t('Enlarge Android test screen','放大 Android 测速界面')}"><img src="assets/screenshots/android-{lang}-speed.jpg" alt="{t('Falcon on Android showing live throughput and protocol metrics','Falcon Android 实时吞吐与协议指标')}" width="802" height="1800" fetchpriority="high"></a></div>
          <p class="visual-caption">{t('Actual app screens. Illustrative test data.','真实应用界面 · 测试数据仅作演示')}</p>
        </div>
      </section>
      <div class="platform-strip container"><p>{t('Native where you work.','在你常用的设备上，原生运行。')}</p><span>iPhone</span><span>iPad</span><span>Mac</span><span>Android</span></div>
      <section class="section container" id="features" aria-labelledby="features-title"><div class="section-heading"><div><p class="eyebrow">{t('One toolkit. Three ways in.','一套工具，三种开测方式')}</p><h2 id="features-title">{t('You choose the connection.','连接方式，由你决定。')}</h2></div><p>{t('Test the route that matters to you, with endpoints and settings you control.','选择你真正关心的链路，掌握对端和测试参数。')}</p></div><div class="workflow-grid">{workflow_html}</div></section>
      <section class="section screens-section" id="screens" aria-labelledby="screens-title"><div class="container"><div class="section-heading"><div><p class="eyebrow">{t('A closer look','看看实际界面')}</p><h2 id="screens-title">{t('From live signal to useful history.','从实时读数，到可复用的历史。')}</h2></div><p>{t('Follow throughput, inspect protocol metrics, and compare runs. Select a platform; tap any screen to enlarge.','观察吞吐曲线、查看协议指标、对比历史结果。选择平台，点击截图即可放大。')}</p></div>
        <div class="screen-tabs" role="tablist" aria-label="{t('Screenshot platform','截图平台')}" hidden><button id="tab-ios" role="tab" aria-controls="screens-ios" aria-selected="true" type="button">iPhone / iPad</button><button id="tab-android" role="tab" aria-controls="screens-android" aria-selected="false" tabindex="-1" type="button">Android</button><button id="tab-mac" role="tab" aria-controls="screens-mac" aria-selected="false" tabindex="-1" type="button">Mac</button></div>{panels}
        <p class="gallery-hint">{t('Swipe to explore more screens →','横向滑动查看更多界面 →')}</p><p class="section-note">{t('Screens show example data and may include Pro features. Appearance varies by device and app version.','截图使用演示数据，部分界面包含 Pro 功能。实际外观随设备与应用版本变化。')}</p>
      </div></section>
      <section class="section container use-cases" id="use-cases" aria-labelledby="cases-title"><div class="section-heading"><div><p class="eyebrow">{t('Built for real networks','面向真实网络')}</p><h2 id="cases-title">{t('Give every test a purpose.','让每次测试，都有明确目标。')}</h2></div><p>{t('A repeatable measurement is a better starting point for understanding a bottleneck.','用可重复的测量，帮助定位网络瓶颈。')}</p></div><div class="use-case-list">{cases_html}</div></section>
      <section class="section pro-section" id="pro" aria-labelledby="pro-title"><div class="container pro-layout"><div class="pro-copy"><p class="eyebrow">Falcon Pro</p><h2 id="pro-title">{t('Go deeper.<br>Buy once.','需要更深入？<br>一次购买，解锁 Pro。')}</h2><p>{t('Start with core testing for free. Add automation and repeatable workflows when you need them.','免费使用核心测速功能，在需要时解锁自动编排与可复用的测试流程。')}</p><a class="text-link" href="{support}#purchases">{t('Purchases & platform details','查看购买与平台说明')} ↗</a><p class="fine-print">{t('Pro purchases are separate on Apple and Google Play. Comparison supports up to 6 runs on Apple and 4 on Android. Prices are shown in your store.','Apple 与 Google Play 的 Pro 需分别购买。Apple 最多对比 6 条记录，Android 最多 4 条。价格以所在商店显示为准。')}</p></div><div class="comparison-wrap"><table class="comparison-table"><caption class="sr-only">{t('Free and Pro features','免费版与 Pro 功能对比')}</caption><thead><tr><th scope="col">{t('What you can do','功能')}</th><th scope="col">{t('Free','免费')}</th><th scope="col">Pro</th></tr></thead><tbody>{rows_html}</tbody></table></div></div></section>
      <section class="section container home-faq" aria-labelledby="faq-title"><div><p class="eyebrow">{t('Good to know','开始之前')}</p><h2 id="faq-title">{t('A few useful answers.','你可能想了解。')}</h2><a class="text-link" href="{support}">{t('Visit the help center','前往帮助中心')} ↗</a></div><div class="faq-list">{faq_html}</div></section>
      <section class="download-section container" id="download" aria-labelledby="download-title"><div class="download-panel"><p class="eyebrow">{t('Ready when you are','准备好，开始测量')}</p><h2 id="download-title">{t('Know your network better.','更了解自己的网络。')}</h2><p>{t('iPhone, iPad, Mac, or Android. Start with the device you already have.','iPhone、iPad、Mac 或 Android，从你手边的设备开始。')}</p>{store_links(lang)}<p class="download-note">{t('iOS / iPadOS 17+ · macOS 14+ on Apple silicon · Android 8+','iOS／iPadOS 17+ · Apple 芯片 Mac，macOS 14+ · Android 8+')}</p></div></section>
    </main>'''


def support(lang):
    t = translate(lang)
    def faq(id_,q,a):
        return f'<details class="faq-item" id="{id_}"><summary>{q}</summary><div class="faq-answer">{a}</div></details>'
    steps = [
        (t('Prepare an endpoint','准备测试对端'),t('On another computer or server, start <code>iperf3 -s</code>. Keep both devices on a reachable network. iPerf2 peers must use iPerf2 on both ends.','在另一台电脑或服务器运行 <code>iperf3 -s</code>，确保两端网络可达。使用 iPerf2 时，两端都必须选择 iPerf2。')),
        (t('Connect in Falcon','在 Falcon 中连接'),t('Open the test target, choose Connect, then enter the peer’s host and port. The usual iPerf3 port is 5201; iPerf2 usually uses 5001.','打开测速目标，选择「连接」，输入对端地址与端口。iPerf3 常用端口为 5201，iPerf2 为 5001。')),
        (t('Run, inspect, repeat','测试、查看、重复'),t('Choose TCP or UDP and your test duration, then start. Review the chart and available metrics. Save a useful run before changing your setup.','选择 TCP 或 UDP、设置测试时长并开始。查看曲线与可用指标，在调整网络配置前保存有价值的结果。')),
    ]
    steps_html = ''.join(f'<li><strong>{title}</strong><p>{text}</p></li>' for title,text in steps)
    general = [
        ('connection',t('Why does a test fail to connect?','为什么测试连不上？'),t('<p>Check the peer address, port, firewall, local-network permission, and network reachability. The other device must already be listening unless you use SSH orchestration. iPerf3 and iPerf2 cannot communicate with each other.</p><p>A successful TCP port check does not prove that a compatible iPerf or UDP service is available.</p>','<p>检查对端地址、端口、防火墙、本地网络权限与网络可达性。除 SSH 编排外，对端应已启动服务。iPerf3 与 iPerf2 不能互通。</p><p>TCP 端口检测成功不代表兼容的 iPerf 或 UDP 服务一定可用。</p>')),
        ('listening',t('Can Falcon act as the server?','Falcon 可以让本机作为服务端吗？'),t('<p>Yes. Choose Listen, set the interface and port, then start. Connect another device to the address Falcon displays. It can accept repeated client sessions until you stop; results follow your automatic or manual saving preference.</p>','<p>可以。选择「监听」，设置接口与端口后启动，让其他设备连接 Falcon 显示的地址。可持续接受多次客户端会话，直到停止；结果按自动或手动保存偏好处理。</p>')),
        ('public-servers',t('Who runs the public servers?','公共服务器由谁运营？'),t('<p>Independent third parties. Falcon does not operate them or guarantee availability, capacity, privacy practices, or supported ports. Respect the operator’s limits. Use your own endpoint for controlled testing.</p>','<p>由独立第三方运营。Falcon 不运营这些服务器，也不保证其可用性、容量、隐私实践或支持端口。请遵守运营方限制；需要受控测量时使用自己的对端。</p>')),
        ('missing-metrics',t('Why are jitter, packet loss, or RTT missing?','为什么缺少抖动、丢包或 RTT？'),t('<p>Metrics depend on the engine, protocol, direction, and peer reports. A dash means no valid value is available; it is not a zero. Some iPerf2 UDP combinations do not return a receiver report.</p>','<p>指标取决于引擎、协议、方向和对端报告。破折号表示没有有效数值，并非零。部分 iPerf2 UDP 组合不会返回接收端报告。</p>')),
        ('ssh',t('What does SSH orchestration do?','SSH 编排具体做什么？'),t('<p>Pro can connect to OpenWrt, Linux, or another compatible SSH host, detect an iPerf engine, start the endpoint, run the test, and clean up. It supports password and OpenSSH private-key authentication, plus explicitly configured credential-free access. Host-key changes require explicit confirmation.</p>','<p>Pro 可连接 OpenWrt、Linux 或其他兼容 SSH 主机，检测 iPerf 引擎、启动对端、运行测试并清理。支持密码、OpenSSH 私钥与明确配置的无凭据访问；主机密钥变化时需要明确确认。</p>')),
    ]
    general_html = ''.join(faq(*entry) for entry in general)
    purchases = ''.join([
        faq('free-pro',t('What is free, and what does Pro add?','免费版包含什么？Pro 增加什么？'),t('<p>Free includes core manual TCP/UDP testing, local server mode, live results, history, individual CSV/JSON exports, and share cards. Pro adds SSH orchestration, advanced graphical parameters and command configuration, saved commands, built-in scenarios and custom presets, saved targets, multi-run comparison, and batch export.</p><p>iPerf3 supports upload, download, and simultaneous bidirectional tests. Direction support varies by engine; use the options available in your installed version.</p>','<p>免费版包含基础手动 TCP／UDP 测试、本机服务端、实时结果、历史、单条 CSV／JSON 导出与分享卡片。Pro 增加 SSH 编排、高级图形参数与命令配置、命令收藏、内置场景与自定义预设、保存常用目标、多记录对比和批量导出。</p><p>iPerf3 支持上传、下载与同时双向测速。方向支持因引擎而异，以已安装版本中的可选项为准。</p>')),
        faq('restore-apple',t('Apple: how do I restore Pro?','Apple：如何恢复 Pro？'),t('<p>Open Settings → Falcon Pro → Restore Purchases. Use the Apple Account that made the purchase. The Apple purchase covers iPhone, iPad, and Mac using that account. It does not unlock the Google Play version.</p>','<p>打开「设置 → Falcon Pro → 恢复购买」，使用原购买的 Apple 账户。Apple 购买可在使用该账户的 iPhone、iPad 与 Mac 上使用，不会解锁 Google Play 版本。</p>')),
        faq('restore-android',t('Android: how do I restore Pro?','Android：如何恢复 Pro？'),t('<p>Open Settings → Falcon Pro → Restore Purchases, using the Google Play account that made the purchase. Check the account and purchase status if access is missing. A pending payment does not unlock Pro. Google Play and Apple purchases are independent.</p>','<p>打开「设置 → Falcon Pro → 恢复购买」，使用原购买的 Google Play 账号。如未恢复，检查账号与订单状态；待付款订单不会解锁 Pro。Google Play 与 Apple 购买相互独立。</p>')),
        faq('refunds',t('How do I request a refund?','如何申请退款？'),t('<p>Use the store where you purchased: <a href="https://reportaproblem.apple.com/">Apple purchase support</a> or <a href="https://support.google.com/googleplay/answer/2479637">Google Play refund help</a>. Eligibility depends on the store’s policies and applicable consumer rights. You may also contact the developer for purchase assistance.</p>','<p>请通过原购买商店处理：<a href="https://reportaproblem.apple.com/">Apple 购买支持</a>或 <a href="https://support.google.com/googleplay/answer/2479637">Google Play 退款帮助</a>。是否符合退款条件取决于商店政策及适用消费者权利，也可联系开发者协助排查购买问题。</p>')),
    ])
    return f'''<section id="quick-start" aria-labelledby="quick-start-title"><h2 id="quick-start-title">{t('Start with a simple test','先完成一次简单测试')}</h2><ol class="quick-steps">{steps_html}</ol><div class="callout"><p>{t('Prefer not to start a server manually? Try a third-party public server in Connect, or use Pro SSH orchestration with your own compatible host. Throughput tests can use substantial data.','不想手动启动服务端？可在「连接」中选择第三方公共服务器，或用 Pro 的 SSH 编排操作自己的兼容主机。吞吐测试可能消耗大量流量。')}</p></div></section>
      <section id="troubleshooting" aria-labelledby="troubleshooting-title"><h2 id="troubleshooting-title">{t('Connections & results','连接与结果')}</h2><div class="faq-list">{general_html}</div></section>
      <section id="platforms" aria-labelledby="platforms-title"><h2 id="platforms-title">{t('Platforms & differences','平台与能力差异')}</h2><div class="platform-help"><article><h3>iPhone / iPad / Mac</h3><p>{t('iOS / iPadOS 17+, or macOS 14+ on Apple silicon. Compare up to 6 saved runs with Pro.','iOS／iPadOS 17+，或 Apple 芯片 Mac，macOS 14+。Pro 最多对比 6 条历史记录。')}</p><a class="text-link" href="{APPLE}">App Store ↗</a></article><article><h3>Android</h3><p>{t('Android 8+. Compare up to 4 saved runs with Pro. Background tests use an ongoing notification and remain subject to Android system limits.','Android 8+。Pro 最多对比 4 条历史记录。后台测试通过持续通知运行，仍受 Android 系统限制。')}</p><a class="text-link" href="{PLAY}">Google Play ↗</a></article></div><p>{t('The app supports Simplified Chinese, Traditional Chinese, English, Japanese, Korean, German, French, Spanish, and Russian. This website is available in English and Simplified Chinese.','应用支持简体中文、繁体中文、英语、日语、韩语、德语、法语、西班牙语与俄语。网站提供英文与简体中文。')}</p></section>
      <section id="purchases" aria-labelledby="purchases-title"><h2 id="purchases-title">{t('Free, Pro & purchases','免费版、Pro 与购买')}</h2><div class="faq-list">{purchases}</div></section>
      <section id="data" aria-labelledby="data-title"><h2 id="data-title">{t('Your data & credentials','数据与凭据')}</h2><p>{t('History, notes, presets, and saved commands are stored locally. Apple SSH credentials use Keychain. Android SSH credentials and known-host data are encrypted with Android Keystore-backed keys and excluded from system backup.','历史、备注、预设与命令收藏保存在本地。Apple SSH 凭据使用 Keychain；Android SSH 凭据与已知主机信息使用 Android Keystore 支持的密钥加密，并排除在系统备份之外。')}</p><p><a href="{route('privacy',lang)}">{t('Read the full privacy policy','阅读完整隐私政策')} ↗</a></p></section>
      <section id="contact" aria-labelledby="contact-title"><h2 id="contact-title">{t('Still need a hand?','仍然需要帮助？')}</h2><p>{t('Send the app version, device and OS version, engine, protocol, direction, and mode (Connect / Listen / SSH). Include the error text and a redacted screenshot if useful. Remove passwords, private keys, and sensitive addresses.','请提供应用版本、设备与系统版本、引擎、协议、方向和模式（连接／监听／SSH），并附上错误文本及有帮助的脱敏截图。移除密码、私钥与敏感地址。')}</p><div class="contact-actions"><a class="button primary" href="mailto:{EMAIL}?subject=Falcon%20support">{t('Email support','发送支持邮件')} {icon('arrow')}</a><button class="button secondary copy-email" type="button" data-copy="{EMAIL}" data-success="{t('Email copied','邮箱已复制')}" data-failure="{t('Select and copy the address below','请选中下方邮箱复制')}" hidden>{t('Copy email address','复制邮箱地址')}</button></div><p class="email-address"><a href="mailto:{EMAIL}">{EMAIL}</a></p><p class="copy-status" role="status" aria-live="polite"></p></section>'''


def metadata(page,lang):
    t=translate(lang)
    return {
        'home':(t('Native network throughput testing','原生网络吞吐测试'),t('Native iPerf3 and iPerf2 testing for iPhone, iPad, Mac, and Android. Live throughput, local server mode, history, and optional SSH orchestration.','面向 iPhone、iPad、Mac 与 Android 的原生 iPerf3／iPerf2 测速工具，支持实时吞吐、本机服务端、历史与可选 SSH 编排。')),
        'support':(t('Help center','帮助中心'),t('Setup, troubleshooting, platform differences, and Apple or Google Play purchase restoration for iPerf Falcon.','iPerf Falcon 设置帮助、故障排查、平台差异与 Apple／Google Play 购买恢复说明。')),
        'privacy':(t('Privacy Policy','隐私政策'),t('How iPerf Falcon handles local data, SSH credentials, network connections, Apple and Google Play purchases, and this website.','了解 iPerf Falcon 如何处理本地数据、SSH 凭据、网络连接、Apple 与 Google Play 购买以及网站访问。')),
        'terms':(t('Terms of Use','使用条款'),t('Terms for iPerf Falcon, including authorized network testing, Apple and Google Play purchases, and third-party services.','iPerf Falcon 使用条款，包含授权网络测试、Apple 与 Google Play 购买以及第三方服务。')),
    }[page]


def document(page,lang,body):
    t=translate(lang)
    title,desc=metadata(page,lang)
    headings=re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',body)
    links=''.join(f'<a href="#{id_}">{re.sub("<[^>]+>","",label)}</a>' for id_,label in headings)
    return f'''<main id="main-content" tabindex="-1" class="document-page container"><header class="document-header"><a class="breadcrumb" href="{route('home',lang)}">← {t('Home','首页')}</a><p class="eyebrow">{t('Help center','帮助中心') if page=='support' else t('Legal information','法律信息')}</p><h1>{title}</h1><p class="updated"><time datetime="{UPDATED}">{updated_label(lang)}</time></p>{f'<p class="document-lead">{desc}</p>' if page=='support' else ''}</header><div class="document-layout"><aside class="toc"><details open><summary>{t('On this page','本页目录')}</summary><nav aria-label="{t('On this page','本页目录')}">{links}</nav></details></aside><article class="document-body">{body}<a class="back-top" href="#main-content">↑ {t('Back to top','返回顶部')}</a></article></div></main>'''


def render(page,lang):
    t=translate(lang)
    title,description=metadata(page,lang)
    filename=route(page,lang)
    canonical=BASE if filename=='index.html' else BASE+filename
    enurl=BASE if page=='home' else BASE+route(page,'en')
    zhurl=BASE+route(page,'zh')
    def asset(path):
        return path+'?v='+hashlib.sha256((ROOT/path).read_bytes()).hexdigest()[:10]
    if page=='home': body=home(lang)
    else:
        content=support(lang) if page=='support' else (ROOT/f'content/{page}.{lang}.html').read_text()
        body=document(page,lang,content)
    return f'''<!DOCTYPE html>
<!-- Generated by scripts/build_site.py; edit the generator or content/ sources. -->
<html lang="{'zh-Hans' if lang=='zh' else 'en'}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(description,quote=True)}">
<meta name="theme-color" content="#f7f8fc" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#0c101b" media="(prefers-color-scheme: dark)">
<title>{escape(title)} · iPerf Falcon</title><link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="en" href="{enurl}"><link rel="alternate" hreflang="zh-Hans" href="{zhurl}"><link rel="alternate" hreflang="x-default" href="{enurl}">
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title)} · iPerf Falcon"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}assets/social-card.png"><meta property="og:locale" content="{'zh_CN' if lang=='zh' else 'en_US'}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="app-icon.png" type="image/png"><link rel="apple-touch-icon" href="app-icon.png"><script src="{asset('theme.js')}"></script><link rel="stylesheet" href="{asset('style.css')}"><script src="{asset('site.js')}" defer></script></head>
<body>{header(page,lang)}{body}{footer(lang)}
<dialog class="lightbox" aria-label="{t('App screenshot preview','应用截图预览')}"><button class="lightbox-close" type="button" aria-label="{t('Close preview','关闭预览')}">×</button><figure><img alt=""><figcaption></figcaption></figure></dialog>
</body></html>
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Fail if tracked output differs from source')
    args=parser.parse_args()
    output={route(page,lang):render(page,lang) for page in ['home','support','privacy','terms'] for lang in ['en','zh']}
    urls=''.join(f'  <url><loc>{BASE if name=="index.html" else BASE+name}</loc><lastmod>{UPDATED}</lastmod></url>\n' for name in output)
    output['sitemap.xml']='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n'
    stale=[]
    for filename,text in output.items():
        target=ROOT/filename
        if args.check:
            if not target.exists() or target.read_text()!=text: stale.append(filename)
        else: target.write_text(text)
    if stale: raise SystemExit('Generated pages need rebuilding: '+', '.join(stale))
    print('Generated output is current.' if args.check else f'Built {len(output)-1} pages and sitemap.xml.')


if __name__=='__main__': main()
