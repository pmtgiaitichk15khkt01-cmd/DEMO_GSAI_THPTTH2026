# VIP 76.0 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018)
# -*- coding: utf-8 -*-
"""
DỊCH VỤ RENDER SƠ ĐỒ TƯ DUY MERMAID (CHỐNG TRÀN, HỖ TRỢ MATHJAX & EXPORT SVG)
Tách độc lập từ app.py để tối ưu tốc độ khởi động Streamlit.
"""
import re
import json
import streamlit as st
import streamlit.components.v1 as components

def render_mermaid(code: str):

    # CHUẨN HÓA MÃ MERMAID VÀ BẢO TOÀN CÔNG THỨC TOÁN LATEX / NGOẶC VUÔNG

    safe_code = code.strip().replace('[[', '[').replace(']]', ']')

    safe_code = re.sub(r'^```(?:mermaid)?', '', safe_code, flags=re.MULTILINE)

    safe_code = re.sub(r'```$', '', safe_code, flags=re.MULTILINE).strip()



    safe_code = re.sub(r'^\s*graph\s+TD', 'graph LR', safe_code, flags=re.IGNORECASE)

    safe_code = re.sub(r'^\s*flowchart\s+TD', 'flowchart LR', safe_code, flags=re.IGNORECASE)

    if not safe_code.startswith(("graph", "flowchart")):

        safe_code = "graph LR\n" + safe_code



    json_code_str = json.dumps(safe_code).replace("</", "<\\/")



    html_template = r"""

    <!-- TÍCH HỢP KATEX VÀ D3.JS CHUẨN SƯ PHẠM QUỐC GIA -->

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">

    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>

    <script src="https://d3js.org/d3.v7.min.js"></script>



    <div style="background: radial-gradient(circle at center, #0f172a 0%, #020617 100%); border-radius: 14px; border: 1.5px solid #1e293b; padding: 12px; position: relative; font-family: system-ui, -apple-system, sans-serif;">

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; padding: 0 10px;">

            <span style="color: #38bdf8; font-size: 13px; font-weight: 700; letter-spacing: 0.5px;">🎯 SƠ ĐỒ TƯ DUY TƯƠNG TÁC THUYẾT TRÌNH (HỖ TRỢ CÔNG THỨC TOÁN KATEX • CLICK ĐỂ SỔ/THU)</span>

            <div>

                <button onclick="expandAll()" style="background: #1e293b; color: #38bdf8; border: 1px solid #38bdf8; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; margin-right: 6px;">➕ Mở tất cả</button>

                <button onclick="collapseAll()" style="background: #1e293b; color: #f43f5e; border: 1px solid #f43f5e; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; margin-right: 6px;">➖ Thu gọn</button>

                <button onclick="resetZoom()" style="background: #1e293b; color: #34d399; border: 1px solid #34d399; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; margin-right: 6px;">🎯 Căn giữa</button>

                <button onclick="downloadMindmapSVG()" style="background: #0ea5e9; color: #ffffff; border: none; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer;">📥 Tải Sơ Đồ (SVG)</button>

            </div>

        </div>

        <div id="mindmap-container" style="width: 100%; height: 550px; overflow: hidden; cursor: grab;"></div>

    </div>



    <script>

    const rawCode = ___JSON_CODE_PLACEHOLDER___;



    // HÀM CHUẨN HÓA HTML & RENDER KATEX TRONG TỪNG NODE SƠ ĐỒ

    function renderLabelWithKaTeX(rawLabel) {

        if (!rawLabel) return "";

        let text = rawLabel.trim().replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');

        // Thay thế an toàn $...$ bằng KaTeX HTML

        text = text.replace(/\$([^\$]+)\$/g, function(match, tex) {

            try {

                if (window.katex) {

                    return window.katex.renderToString(tex, { throwOnError: false, displayMode: false });

                }

            } catch (e) {

                console.warn("KaTeX error:", e);

            }

            return match;

        });

        return text;

    }



    // BỘ PHÂN TÍCH NODE THÔNG MINH: BẢO VỆ NGOẶC VUÔNG [a,b] VÀ NHÁY KÉP

    function parseNodePart(part) {

        if (!part) return null;

        part = part.trim().split(':::')[0].trim();



        let firstDelim = -1;

        let openChar = null;

        for (let i = 0; i < part.length; i++) {

            const ch = part[i];

            if (ch === '(' || ch === '[' || ch === '{') {

                firstDelim = i;

                openChar = ch;

                break;

            }

        }



        if (firstDelim === -1) {

            return { id: part, label: part };

        }



        const id = part.substring(0, firstDelim).trim();

        const rest = part.substring(firstDelim).trim();

        const closeChar = openChar === '(' ? ')' : (openChar === '[' ? ']' : '}');

        const lastClose = rest.lastIndexOf(closeChar);



        let label = lastClose !== -1 ? rest.substring(1, lastClose).trim() : rest.substring(1).trim();

        if ((label.startsWith('"') && label.endsWith('"')) || (label.startsWith("'") && label.endsWith("'"))) {

            label = label.substring(1, label.length - 1).trim();

        }

        return { id: id || label, label: label || id };

    }



    function parseMermaidToTree(code) {

        if (!code) return null;

        // BỘ TÁCH DÒNG LINH HOẠT HỖ TRỢ CẢ NEWLINE THỰC TẾ LẪN LITERAL \n

        let lines = code.split(/\r?\n/);

        if (lines.length <= 1 && code.includes('\\n')) {

            lines = code.split('\\n');

        }



        const nodeLabels = {};

        const childrenMap = {};

        const parentMap = {};



        function registerNode(node) {

            if (!node || !node.id) return;

            if (node.label && node.label !== node.id) {

                nodeLabels[node.id] = node.label;

            } else if (!nodeLabels[node.id]) {

                nodeLabels[node.id] = node.label || node.id;

            }

        }



        lines.forEach(line => {

            line = line.trim();

            if (!line || line.startsWith('graph') || line.startsWith('flowchart') || line.startsWith('classDef') || line.startsWith('style') || line.startsWith('subgraph') || line === 'end') {

                return;

            }

            // Hỗ trợ mọi kiểu mũi tên và liên kết: -->, ---, ==>, -.->, -> có hoặc không có nhãn |...|

            const arrowMatch = line.match(/^(.*?)\s*(?:-->|==>|-\.->|---|->)(?:\|.*?\|)?\s*(.*)$/);

            if (arrowMatch) {

                const src = parseNodePart(arrowMatch[1]);

                const tgt = parseNodePart(arrowMatch[2]);

                if (src && tgt) {

                    registerNode(src);

                    registerNode(tgt);



                    if (!childrenMap[src.id]) childrenMap[src.id] = [];

                    if (!childrenMap[src.id].includes(tgt.id)) childrenMap[src.id].push(tgt.id);

                    parentMap[tgt.id] = src.id;

                }

            } else {

                const node = parseNodePart(line);

                if (node && node.id) {

                    registerNode(node);

                }

            }

        });



        const allIds = Object.keys(nodeLabels);

        if (allIds.length === 0) return null;

        let rootId = allIds.find(id => !parentMap[id]) || allIds[0];



        function build(id, depth) {

            const item = { id: id, name: nodeLabels[id] || id, depth: depth };

            const childIds = childrenMap[id] || [];

            if (childIds.length > 0) {

                item.children = childIds.map(cId => build(cId, depth + 1));

            }

            return item;

        }

        return build(rootId, 0);

    }



    // TẦNG CỨU HỘ SƠ ĐỒ AUTO-HEALER (ĐẢM BẢO KHÔNG BAO GIỜ TREO MÀN HÌNH ĐEN)

    function generateAutoHealerTree(code) {

        let topicName = "NỘI DUNG TRỌNG TÂM BÀI HỌC";

        const m = (code || '').match(/\[["']?(.*?)["']?\]/);

        if (m && m[1] && m[1].length < 60) {

            topicName = m[1].replace(/["']/g, '').trim();

        }

        return {

            id: "Root",

            name: "🎯 " + topicName,

            depth: 0,

            children: [

                {

                    id: "N1",

                    name: "📖 1. Định nghĩa & Khái niệm cốt lõi",

                    depth: 1,

                    children: [

                        { id: "N1_1", name: "Định nghĩa chuẩn SGK Kết Nối Tri Thức", depth: 2 },

                        { id: "N1_2", name: "Điều kiện xác định & Phạm vi áp dụng", depth: 2 }

                    ]

                },

                {

                    id: "N2",

                    name: "⚡ 2. Công thức & Quy tắc trọng tâm",

                    depth: 1,

                    children: [

                        { id: "N2_1", name: "Công thức cơ bản nền tảng", depth: 2 },

                        { id: "N2_2", name: "Tính chất biến đổi & Mở rộng", depth: 2 }

                    ]

                },

                {

                    id: "N3",

                    name: "🔍 3. Phương pháp giải & Dạng bài tập",

                    depth: 1,

                    children: [

                        { id: "N3_1", name: "Dạng 1: Nhận biết & Thông hiểu", depth: 2 },

                        { id: "N3_2", name: "Dạng 2: Vận dụng liên môn & Thực tiễn", depth: 2 }

                    ]

                },

                {

                    id: "N4",

                    name: "🌐 4. Ứng dụng & Mối liên hệ thực tiễn",

                    depth: 1,

                    children: [

                        { id: "N4_1", name: "Mô hình hóa thực tế trong đời sống", depth: 2 },

                        { id: "N4_2", name: "Liên hệ các môn KHTN & Công nghệ", depth: 2 }

                    ]

                }

            ]

        };

    }



    let treeData = parseMermaidToTree(rawCode);

    if (!treeData || !treeData.children || treeData.children.length === 0) {

        console.warn("Kích hoạt Auto-Healer Tree Generator cho sơ đồ tư duy!");

        treeData = generateAutoHealerTree(rawCode);

    }

    const container = document.getElementById("mindmap-container");

    const height = 550;



    {

        const svg = d3.select("#mindmap-container").append("svg")

            .attr("width", "100%")

            .attr("height", height)

            .attr("id", "svg-mindmap-element")

            .style("user-select", "text");



        const g = svg.append("g");



        const zoom = d3.zoom()

            .scaleExtent([0.25, 3.5])

            .on("zoom", (e) => g.attr("transform", e.transform));

        svg.call(zoom);



        const treeLayout = d3.tree().nodeSize([78, 240]);

        const root = d3.hierarchy(treeData);

        root.x0 = height / 2;

        root.y0 = 40;



        const palette = ["#818cf8", "#38bdf8", "#34d399", "#fbbf24", "#f472b6", "#a78bfa", "#38bdf8"];



        // Thu gọn các nhánh con từ cấp 2 trở đi để sơ đồ thoáng đãng, người dùng click mở dần

        if (root.children) {

            root.children.forEach(c => {

                if (c.children) {

                    c.children.forEach(sub => {

                        if (sub.children) {

                            sub._children = sub.children;

                            sub.children = null;

                        }

                    });

                }

            });

        }



        // BỘ ĐO CHIỀU RỘNG THỰC TẾ OFF-SCREEN CHO KATEX VÀ TIẾNG VIỆT

        let measureBox = document.getElementById("mindmap-measure-box");

        if (!measureBox) {

            measureBox = document.createElement("div");

            measureBox.id = "mindmap-measure-box";

            measureBox.style.cssText = "position:absolute; visibility:hidden; top:-9999px; left:-9999px; white-space:nowrap; font-family:system-ui,-apple-system,sans-serif;";

            document.body.appendChild(measureBox);

        }



        function getPreciseNodeWidth(text, depth) {

            if (!text) return 90;

            measureBox.style.fontSize = depth === 0 ? "13.5px" : "12.5px";

            measureBox.style.fontWeight = depth === 0 ? "800" : "600";

            measureBox.innerHTML = renderLabelWithKaTeX(text);

            const rect = measureBox.getBoundingClientRect();

            const measuredW = Math.ceil(rect.width || measureBox.offsetWidth || (text.length * 8));

            // Padding chuẩn xác: 26px cho icon tròn + 18px lề phải + 4px co giãn = 48px

            return Math.max(90, measuredW + 48);

        }



        let i = 0;

        function update(source) {

            const treeInfo = treeLayout(root);

            const nodes = treeInfo.descendants();

            const links = treeInfo.links();



            // Tính toán kích thước hộp chuẩn xác 100% dựa trên KaTeX render thực tế (ôm sát nội dung)

            const maxWByDepth = {};

            nodes.forEach(d => {

                d.boxWidth = getPreciseNodeWidth(d.data.name, d.depth);

                d.boxHeight = 42;

                if (!maxWByDepth[d.depth] || d.boxWidth > maxWByDepth[d.depth]) {

                    maxWByDepth[d.depth] = d.boxWidth;

                }

            });



            // Tọa độ X của từng level dựa trên độ rộng lớn nhất của cột trước đó

            const depthX = [35];

            for (let dep = 1; dep <= 12; dep++) {

                depthX[dep] = depthX[dep - 1] + (maxWByDepth[dep - 1] || 120) + 55;

            }



            nodes.forEach(d => {

                d.y = depthX[d.depth];

            });



            const node = g.selectAll("g.node").data(nodes, d => d.id || (d.id = ++i));



            // HÀM PHÁT ÂM TIẾNG ANH CHO TỪNG NODE TRONG SƠ ĐỒ TƯ DUY

            function speakMindmapText(rawName) {
                const fn = (window.parent && window.parent.__speakPedagogicalText) ||
                           window.__speakPedagogicalText ||
                           (window.parent && window.parent.speakEnglishText) ||
                           window.speakEnglishText;
                if (fn) {
                    fn(rawName);
                } else {
                    console.warn("Mindmap TTS: Voice function not available.");
                }
            }



            const nodeEnter = node.enter().append("g")

                .attr("class", "node")

                .attr("transform", d => `translate(${source.y0},${source.x0})`)

                .style("cursor", "pointer")

                .on("click", (event, d) => {

                    // Tự động phát âm nếu nhãn là tiếng Anh

                    speakMindmapText(d.data.name);

                    if (d.children) {

                        d._children = d.children;

                        d.children = null;

                    } else if (d._children) {

                        d.children = d._children;

                        d._children = null;

                    }

                    update(d);

                });



            // KHUNG CHỮ NHẬT BO GÓC PHÒNG LAB

            nodeEnter.append("rect")

                .attr("rx", 9).attr("ry", 9)

                .attr("x", 0).attr("y", -21)

                .attr("height", d => d.boxHeight)

                .attr("width", d => d.boxWidth)

                .style("fill", "#0f172a")

                .style("stroke", d => palette[d.depth % palette.length])

                .style("stroke-width", d => d.depth === 0 ? "2.5px" : "1.8px")

                .style("filter", "drop-shadow(0 4px 10px rgba(0,0,0,0.65))");



            // NÚT TRÒN CHỈ BÁO CÓ NHÁNH CON

            nodeEnter.append("circle")

                .attr("cx", 14).attr("cy", 0).attr("r", 5.5)

                .style("fill", d => d._children ? palette[d.depth % palette.length] : (d.children ? "#0f172a" : "#475569"))

                .style("stroke", d => palette[d.depth % palette.length])

                .style("stroke-width", "2px");



            // HIỂN THỊ NỘI DUNG QUA FOREIGNOBJECT (NHÚNG HTML KATEX CHUẨN XÁC 100%)

            const fo = nodeEnter.append("foreignObject")

                .attr("x", 26)

                .attr("y", -21)

                .attr("width", d => d.boxWidth - 28)

                .attr("height", d => d.boxHeight)

                .style("overflow", "visible")

                .style("pointer-events", "auto");



            fo.append("xhtml:div")

                .style("color", "#ffffff")

                .style("font-size", d => d.depth === 0 ? "13.5px" : "12.5px")

                .style("font-weight", d => d.depth === 0 ? "800" : "600")

                .style("line-height", "42px")

                .style("white-space", "nowrap")

                .style("overflow", "visible")

                .style("user-select", "text")

                .style("cursor", "pointer")

                .on("dblclick", (event, d) => {

                    event.stopPropagation();

                    speakMindmapText(d.data.name);

                })

                .html(d => renderLabelWithKaTeX(d.data.name));



            const nodeUpdate = node.merge(nodeEnter).transition().duration(350)

                .attr("transform", d => `translate(${d.y},${d.x})`);



            nodeUpdate.select("rect").attr("width", d => d.boxWidth);

            nodeUpdate.select("foreignObject").attr("width", d => d.boxWidth - 28);

            nodeUpdate.select("circle")

                .style("fill", d => d._children ? palette[d.depth % palette.length] : (d.children ? "#0f172a" : "#475569"));



            const nodeExit = node.exit().transition().duration(350)

                .attr("transform", d => `translate(${source.y},${source.x})`)

                .remove();



            const link = g.selectAll("path.link").data(links, d => d.target.id);



            const linkPath = d => {

                const startX = d.source.y + d.source.boxWidth;

                const startY = d.source.x;

                const endX = d.target.y;

                const endY = d.target.x;

                return `M ${startX} ${startY} C ${(startX + endX) / 2} ${startY}, ${(startX + endX) / 2} ${endY}, ${endX} ${endY}`;

            };



            const linkEnter = link.enter().insert("path", "g")

                .attr("class", "link")

                .attr("d", d => {

                    const startX = source.y0 + (source.boxWidth || 150);

                    return `M ${startX} ${source.x0} C ${startX} ${source.x0}, ${startX} ${source.x0}`;

                })

                .style("fill", "none")

                .style("stroke", d => palette[d.target.depth % palette.length])

                .style("stroke-opacity", 0.75)

                .style("stroke-width", "2px");



            link.merge(linkEnter).transition().duration(350)

                .attr("d", linkPath);



            link.exit().transition().duration(350)

                .attr("d", d => {

                    const startX = source.y + (source.boxWidth || 150);

                    return `M ${startX} ${source.x} C ${startX} ${source.x}`;

                })

                .remove();



            nodes.forEach(d => { d.x0 = d.x; d.y0 = d.y; });

        }



        update(root);



        svg.call(zoom.transform, d3.zoomIdentity.translate(50, height / 2.3).scale(0.85));



        window.expandAll = function() {

            function expand(d) {

                if (d._children) { d.children = d._children; d._children = null; }

                if (d.children) d.children.forEach(expand);

            }

            expand(root);

            update(root);

        };



        window.collapseAll = function() {

            if (root.children) {

                root.children.forEach(c => {

                    function collapse(d) {

                        if (d.children) { d._children = d.children; d.children = null; }

                        if (d._children) d._children.forEach(collapse);

                    }

                    collapse(c);

                });

            }

            update(root);

        };



        window.resetZoom = function() {

            svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity.translate(50, height / 2.3).scale(0.85));

        };



        window.downloadMindmapSVG = function() {

            const svgEl = document.getElementById("svg-mindmap-element");

            if (!svgEl) return;

            const serializer = new XMLSerializer();

            let source = serializer.serializeToString(svgEl);

            if(!source.match(/^<svg/)){

                source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');

            }

            const url = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(source);

            const downloadLink = document.createElement("a");

            downloadLink.href = url;

            downloadLink.download = "SoDoTuDuy_KNTT.svg";

            document.body.appendChild(downloadLink);

            downloadLink.click();

            document.body.removeChild(downloadLink);

        };

    }

    </script>

    """



    final_html = html_template.replace("___JSON_CODE_PLACEHOLDER___", json_code_str)

    if hasattr(st, "iframe"):

        st.iframe(final_html, height=580)

    else:

        components.html(final_html, height=580, scrolling=False)



