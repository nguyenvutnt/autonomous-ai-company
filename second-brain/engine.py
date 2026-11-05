"""
3-Tier Corporate Second Brain Engine for the 16-Department Autonomous AI Company.

Architecture:
- Tier 1 (SQLite WAL + FTS5 BM25): Instant structured facts, SOPs, product catalog,
  brand rules, financial ledger, and cross-compatible with `SqliteAiMemoryStore` (`ai_memories`).
- Tier 2 (Episodic & Kaizen Self-Learning Layer — mem0 compatible): Captures department/agent
  campaign outcomes, winning hooks, failed experiments, and auto-distills lessons across all 16 departments.
- Tier 3 (Knowledge Graph & Entity RAG — LightRAG + NetworkX compatible): Builds an entity-relation
  graph (Product <-> Keyword <-> Competitor <-> Audience <-> Channel <-> Hook) with multi-hop traversal
  for SEO/AIO/SAO citation engineering and cross-department context retrieval.
"""

from __future__ import annotations

import json
import os
import sqlite3
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import networkx as nx

DEFAULT_DB_PATH = os.environ.get(
    "SECOND_BRAIN_DB_PATH",
    "/root/ecosystem/second-brain/data/corporate_second_brain.db",
)

# 11 Memory Categories (0..6 match Facebook.Net SqliteAiMemoryStore + 7..10 Corporate Extensions)
MEMORY_CATEGORIES: dict[str, int] = {
    "General": 0,
    "UserPreference": 1,
    "ProductKnowledge": 2,
    "WritingStyle": 3,
    "CampaignRule": 4,
    "GroupStrategy": 5,
    "LeadPlaybook": 6,
    "DepartmentSop": 7,
    "KaizenLesson": 8,
    "EntityGraph": 9,
    "FinanceLedger": 10,
    "MediaAssetVault": 11,
}

CATEGORY_ID_TO_NAME: dict[int, str] = {v: k for k, v in MEMORY_CATEGORIES.items()}

# 16 Official AI Company Departments
CORPORATE_DEPARTMENTS: dict[str, dict[str, str]] = {
    "01_ceo": {
        "name": "CEO & Chief of Staff",
        "role": "Chiến lược tổng thể 30-90 ngày, giao KPI, duyệt ngân sách & nghiệm thu liên phòng ban",
        "profile_ref": "specialized/specialized-chief-of-staff.md",
        "weapons": "n8n, MetaGPT, crewAI, CorporateSecondBrain",
    },
    "02_creative_director": {
        "name": "Giám Đốc Sáng Tạo (Creative Director)",
        "role": "Định hình Concept, duyệt Hook 3s đầu, kiểm soát Brand Voice & tính thẩm mỹ",
        "profile_ref": "paid-media/paid-media-creative-strategist.md",
        "weapons": "CorporateSecondBrain Brand Memory,agency-agents",
    },
    "03_design": {
        "name": "Nhân Sự Design (Visual & Prompt Studio)",
        "role": "Tạo ảnh sản phẩm studio, giữ đồng nhất khuôn mặt mẫu ảo, vẽ Thumbnail, đóng dấu Watermark",
        "profile_ref": "design/design-image-prompt-engineer.md",
        "weapons": "ComfyUI, ImageSharp",
    },
    "04_content": {
        "name": "Nhân Sự Content (Copywriter & Scriptwriter)",
        "role": "Viết bài chuyên sâu 5-Tier E-E-A-T, kịch bản video viral, Carousel & Spintax 200x",
        "profile_ref": "marketing/marketing-content-creator.md",
        "weapons": "gpt-researcher, Spintax Engine",
    },
    "05_media_livestream": {
        "name": "Nhân Sự Media & Livestream 24/7",
        "role": "Lồng tiếng AI Tiếng Việt tự nhiên, điều khiển Streamer ảo phát sóng Livestream 24/7",
        "profile_ref": "marketing/marketing-livestream-commerce-coach.md",
        "weapons": "LivePortrait, edge-tts, faster-whisper, mediamtx, srs",
    },
    "06_video_editor": {
        "name": "Nhân Sự Dựng Phim (Short Video Editor)",
        "role": "Tải video Douyin/TikTok không logo, Việt hóa, tự dựng Shorts/Reels, gắn sub karaoke",
        "profile_ref": "marketing/marketing-short-video-editing-coach.md",
        "weapons": "OpenMontage (77k★), MoneyPrinterTurbo, pyvideotrans, NarratoAI, Douyin_TikTok_Download_API",
    },
    "07_seo": {
        "name": "Nhân Viên SEO (Google & Web Organic)",
        "role": "Quét từ khóa GSC, xây dựng Topic Clusters, Internal Link tự động & Google Fast Index",
        "profile_ref": "marketing/marketing-seo-specialist.md",
        "weapons": "crawl4ai, firecrawl, WordPress/Shopify API",
    },
    "08_aio": {
        "name": "Nhân Viên AIO (AEO / GEO Citation Engineer)",
        "role": "Tối ưu câu trả lời trực tiếp & Entity Graph để ChatGPT, Perplexity, Gemini trích dẫn",
        "profile_ref": "marketing/marketing-aeo-foundations.md",
        "weapons": "crawl4ai, LightRAG Entity Graph, JSON-LD Schema",
    },
    "09_sao": {
        "name": "Nhân Viên SAO (Social & Agentic Search Optimizer)",
        "role": "Tối ưu tìm kiếm trên TikTok Search, FB Search, YouTube/Shopee Search & AI Shopping Agents",
        "profile_ref": "marketing/marketing-agentic-search-optimizer.md",
        "weapons": "Douyin_TikTok_Download_API, Facebook.Net, postiz-app",
    },
    "10_social": {
        "name": "Nhân Viên Social (Multi-Channel & Account Farm)",
        "role": "Nuôi dàn nick chống Checkpoint, dùng Page Admin rải bài Group & đăng 12 mạng xã hội",
        "profile_ref": "marketing/marketing-social-media-strategist.md",
        "weapons": "postiz-app, Facebook.Net, Camoufox, browser-use",
    },
    "11_ads": {
        "name": "Nhân Viên Ads (Paid Media & Viral Seeding)",
        "role": "Lên chiến dịch Ads, điều khiển dàn nick Seeding chéo, Auto Up tin Group & Seeding Live",
        "profile_ref": "paid-media/paid-media-paid-social-strategist.md",
        "weapons": "Facebook.Net Seeding, Ads Tracking",
    },
    "12_sale": {
        "name": "Nhân Viên Sale & CSKH (Lead Hunter & Closer)",
        "role": "Quét UID/SĐT/Email từ đối thủ, tự động kết bạn Zalo/FB, bắn Inbox/Email & chốt đơn 24/7",
        "profile_ref": "sales/sales-outbound-strategist.md",
        "weapons": "Twenty CRM (60k★), Facebook.Net Scanner, Zalo.Net, chatwoot, listmonk",
    },
    "13_cfo": {
        "name": "CFO (Giám Đốc Tài Chính)",
        "role": "Phân tích hiệu quả tài chính, tính ROAS/ROI từng chiến dịch, tối ưu định giá & ngân sách",
        "profile_ref": "finance/finance-fpa-analyst.md",
        "weapons": "CorporateSecondBrain FinanceLedger",
    },
    "14_accountant": {
        "name": "Nhân Viên Kế Toán (Bookkeeper & Replay Audit)",
        "role": "Hạch toán thu-chi, kiểm soát chi phí Proxy/Ads, quản lý video đóng gói hàng đối soát",
        "profile_ref": "finance/finance-bookkeeper-controller.md",
        "weapons": "CorporateSecondBrain FinanceLedger, FFmpeg Simple Replay",
    },
    "15_hr": {
        "name": "Giám Đốc Nhân Sự (HR & Agent Prompt Kaizen)",
        "role": "Tuyển dụng Agent từ kho 330 hồ sơ, chấm KPI từng phòng ban & tự động tinh chỉnh Prompt",
        "profile_ref": "specialized/operations-manager.md",
        "weapons": "agency-agents (330 profiles), CorporateSecondBrain KaizenLesson",
    },
    "16_it": {
        "name": "Giám Đốc IT / DevOps & Security",
        "role": "Giám sát uptime 26 repos, xoay Proxy, sinh mã 2FA, dùng browser-use tự sửa lỗi giao diện",
        "profile_ref": "engineering/engineering-devops-automator.md",
        "weapons": "n8n, Camoufox, browser-use, skyvern",
    },
}


def _strip_accents(text: str) -> str:
    """Normalizes Vietnamese accents for accent-insensitive full-text indexing."""
    if not text:
        return ""
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return stripped.replace("đ", "d").replace("Đ", "D").lower()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class CorporateSecondBrain:
    """
    3-Tier Hybrid Corporate Second Brain for the 16-Department AI Factory.
    """

    def __init__(self, db_path: str = DEFAULT_DB_PATH) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.lightrag_dir = self.db_path.parent / "lightrag_storage"
        self.lightrag_dir.mkdir(parents=True, exist_ok=True)
        self._init_schema()
        self._seed_departments_if_empty()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=15.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA temp_store=MEMORY;")
        conn.execute("PRAGMA busy_timeout=5000;")
        return conn

    def _init_schema(self) -> None:
        sql = """
        -- Tier 1: Core Memories (100% compatible with Facebook.Net SqliteAiMemoryStore)
        CREATE TABLE IF NOT EXISTS ai_memories (
            id TEXT PRIMARY KEY,
            category INTEGER NOT NULL,
            mem_key TEXT NOT NULL,
            content TEXT NOT NULL,
            importance INTEGER NOT NULL DEFAULT 3,
            account_uid TEXT,
            department TEXT DEFAULT 'all',
            tags TEXT DEFAULT '',
            normalized_search TEXT DEFAULT '',
            created_at_utc TEXT NOT NULL,
            updated_at_utc TEXT NOT NULL
        );

        CREATE UNIQUE INDEX IF NOT EXISTS idx_ai_memories_cat_lower_key
            ON ai_memories(category, LOWER(mem_key));

        CREATE INDEX IF NOT EXISTS idx_ai_memories_importance
            ON ai_memories(importance DESC, updated_at_utc DESC);

        -- FTS5 Virtual Table for sub-millisecond BM25 search across Tier 1
        CREATE VIRTUAL TABLE IF NOT EXISTS ai_memories_fts USING fts5(
            mem_id UNINDEXED,
            mem_key,
            content,
            department,
            tags,
            normalized_search
        );

        -- Tier 2: Episodic & Kaizen Self-Learning Memory (mem0 style)
        CREATE TABLE IF NOT EXISTS kaizen_lessons (
            id TEXT PRIMARY KEY,
            department TEXT NOT NULL,
            campaign_or_task TEXT NOT NULL,
            action_taken TEXT NOT NULL,
            outcome_status TEXT NOT NULL, -- 'WIN', 'LOSS', 'INSIGHT'
            metrics_json TEXT NOT NULL DEFAULT '{}',
            extracted_rule TEXT NOT NULL,
            importance INTEGER NOT NULL DEFAULT 4,
            applied_to_departments TEXT NOT NULL DEFAULT 'all',
            created_at_utc TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_kaizen_dept_outcome
            ON kaizen_lessons(department, outcome_status, importance DESC);

        -- Tier 3: Knowledge Graph Entities & Relations (LightRAG + NetworkX compatible)
        CREATE TABLE IF NOT EXISTS kg_entities (
            entity_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            entity_type TEXT NOT NULL, -- 'Product', 'Keyword', 'Competitor', 'Persona', 'Channel', 'Hook', 'Topic'
            description TEXT NOT NULL,
            attributes_json TEXT NOT NULL DEFAULT '{}',
            department TEXT NOT NULL DEFAULT 'all',
            updated_at_utc TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_kg_entities_type
            ON kg_entities(entity_type);

        CREATE TABLE IF NOT EXISTS kg_relations (
            relation_id TEXT PRIMARY KEY,
            source_id TEXT NOT NULL,
            target_id TEXT NOT NULL,
            relation_type TEXT NOT NULL, -- 'TARGETS_KEYWORD', 'COMPETES_WITH', 'SOLVES_PAIN', 'USES_HOOK', 'RANKS_ON'
            weight REAL NOT NULL DEFAULT 1.0,
            evidence TEXT NOT NULL DEFAULT '',
            updated_at_utc TEXT NOT NULL,
            UNIQUE(source_id, target_id, relation_type)
        );

        CREATE INDEX IF NOT EXISTS idx_kg_relations_src
            ON kg_relations(source_id);
        CREATE INDEX IF NOT EXISTS idx_kg_relations_tgt
            ON kg_relations(target_id);

        -- Corporate Financial & KPI Ledger (For CFO #13 & Accountant #14)
        CREATE TABLE IF NOT EXISTS finance_ledger (
            tx_id TEXT PRIMARY KEY,
            department TEXT NOT NULL,
            campaign_id TEXT NOT NULL,
            tx_type TEXT NOT NULL, -- 'REVENUE', 'AD_SPEND', 'PROXY_COST', 'TOOL_COST', 'REFUND'
            amount_vnd REAL NOT NULL,
            leads_count INTEGER NOT NULL DEFAULT 0,
            orders_count INTEGER NOT NULL DEFAULT 0,
            note TEXT NOT NULL DEFAULT '',
            created_at_utc TEXT NOT NULL
        );
        """
        with self._connect() as conn:
            conn.executescript(sql)
            # Ensure backward-compatible columns if syncing with an existing facebook_ai_memory.db
            for col_def in [
                "department TEXT DEFAULT 'all'",
                "tags TEXT DEFAULT ''",
                "normalized_search TEXT DEFAULT ''",
            ]:
                try:
                    conn.execute(f"ALTER TABLE ai_memories ADD COLUMN {col_def};")
                except sqlite3.OperationalError:
                    pass

    def _seed_departments_if_empty(self) -> None:
        """Seeds the 16 AI Company Department SOP profiles into Tier 1 if not yet present."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS cnt FROM ai_memories WHERE category = ?",
                (MEMORY_CATEGORIES["DepartmentSop"],),
            ).fetchone()
            if row and row["cnt"] >= 16:
                return

        for dept_id, info in CORPORATE_DEPARTMENTS.items():
            content = (
                f"Chức danh: {info['name']} | "
                f"Nhiệm vụ SOP: {info['role']} | "
                f"Vũ khí: {info['weapons']} | "
                f"Hồ sơ gốc: {info['profile_ref']}"
            )
            self.save_memory(
                category="DepartmentSop",
                key=f"sop_{dept_id}",
                content=content,
                importance=5,
                department=dept_id,
                tags="sop,department,organization",
            )

    # =========================================================================
    # TIER 1: STRUCTURED & BM25 FULL-TEXT MEMORY
    # =========================================================================
    def save_memory(
        self,
        category: str | int,
        key: str,
        content: str,
        importance: int = 3,
        department: str = "all",
        tags: str = "",
        account_uid: str | None = None,
    ) -> dict[str, Any]:
        """Atomically upserts a Tier 1 memory and indexes it in SQLite FTS5."""
        if isinstance(category, str):
            cat_id = MEMORY_CATEGORIES.get(category, MEMORY_CATEGORIES["General"])
            cat_name = category if category in MEMORY_CATEGORIES else "General"
        else:
            cat_id = int(category)
            cat_name = CATEGORY_ID_TO_NAME.get(cat_id, "General")

        clean_key = key.strip()
        clean_content = content.strip()
        clamped_imp = max(1, min(5, int(importance)))
        now_iso = _utc_now_iso()
        new_id = f"mem_{uuid.uuid4().hex}"
        norm_text = _strip_accents(f"{clean_key} {clean_content} {department} {tags}")

        with self._connect() as conn:
            row = conn.execute(
                """
                INSERT INTO ai_memories (
                    id, category, mem_key, content, importance, account_uid,
                    department, tags, normalized_search, created_at_utc, updated_at_utc
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(category, LOWER(mem_key)) DO UPDATE SET
                    content = excluded.content,
                    importance = excluded.importance,
                    account_uid = COALESCE(excluded.account_uid, ai_memories.account_uid),
                    department = excluded.department,
                    tags = excluded.tags,
                    normalized_search = excluded.normalized_search,
                    updated_at_utc = excluded.updated_at_utc
                RETURNING id, category, mem_key, content, importance, department, tags, updated_at_utc;
                """,
                (
                    new_id,
                    cat_id,
                    clean_key,
                    clean_content,
                    clamped_imp,
                    account_uid,
                    department,
                    tags,
                    norm_text,
                    now_iso,
                    now_iso,
                ),
            ).fetchone()

            mem_id = row["id"]
            conn.execute("DELETE FROM ai_memories_fts WHERE mem_id = ?;", (mem_id,))
            conn.execute(
                """
                INSERT INTO ai_memories_fts (mem_id, mem_key, content, department, tags, normalized_search)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (mem_id, clean_key, clean_content, department, tags, norm_text),
            )

        return {
            "id": row["id"],
            "category": cat_name,
            "category_id": row["category"],
            "key": row["mem_key"],
            "content": row["content"],
            "importance": row["importance"],
            "department": row["department"],
            "tags": row["tags"],
            "updated_at_utc": row["updated_at_utc"],
        }

    def query_memories(
        self,
        keyword: str | None = None,
        category: str | int | None = None,
        department: str | None = None,
        limit: int = 25,
    ) -> list[dict[str, Any]]:
        """Queries Tier 1 memories using hybrid FTS5 BM25 + accent-insensitive matching."""
        cat_id: int | None = None
        if isinstance(category, str) and category in MEMORY_CATEGORIES:
            cat_id = MEMORY_CATEGORIES[category]
        elif isinstance(category, int):
            cat_id = category

        with self._connect() as conn:
            if keyword and keyword.strip():
                norm_kw = _strip_accents(keyword.strip())
                tokens = [t for t in norm_kw.split() if t]
                fts_query = " OR ".join(f'"{t}"*' for t in tokens)
                rows = conn.execute(
                    """
                    SELECT m.id, m.category, m.mem_key, m.content, m.importance,
                           m.department, m.tags, m.updated_at_utc,
                           bm25(ai_memories_fts) AS rank_score
                    FROM ai_memories_fts f
                    JOIN ai_memories m ON m.id = f.mem_id
                    WHERE ai_memories_fts MATCH ?
                      AND (? IS NULL OR m.category = ?)
                      AND (? IS NULL OR m.department = 'all' OR m.department = ?)
                    ORDER BY m.importance DESC, rank_score ASC, m.updated_at_utc DESC
                    LIMIT ?;
                    """,
                    (fts_query, cat_id, cat_id, department, department, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT id, category, mem_key, content, importance,
                           department, tags, updated_at_utc
                    FROM ai_memories
                    WHERE (? IS NULL OR category = ?)
                      AND (? IS NULL OR department = 'all' OR department = ?)
                    ORDER BY importance DESC, updated_at_utc DESC
                    LIMIT ?;
                    """,
                    (cat_id, cat_id, department, department, limit),
                ).fetchall()

        return [
            {
                "id": r["id"],
                "category": CATEGORY_ID_TO_NAME.get(r["category"], "General"),
                "key": r["mem_key"],
                "content": r["content"],
                "importance": r["importance"],
                "department": r["department"],
                "tags": r["tags"],
                "updated_at_utc": r["updated_at_utc"],
            }
            for r in rows
        ]

    # =========================================================================
    # TIER 2: KAIZEN & EPISODIC SELF-LEARNING MEMORY (mem0 style)
    # =========================================================================
    def record_kaizen_lesson(
        self,
        department: str,
        campaign_or_task: str,
        action_taken: str,
        outcome_status: str,
        extracted_rule: str,
        metrics: dict[str, Any] | None = None,
        importance: int = 4,
        applied_to_departments: str = "all",
    ) -> dict[str, Any]:
        """
        Records a practical Kaizen lesson after running a task/campaign and automatically
        promotes high-importance rules into Tier 1 shared memory so all 16 departments learn immediately.
        """
        lesson_id = f"kz_{uuid.uuid4().hex[:12]}"
        now_iso = _utc_now_iso()
        status_clean = outcome_status.upper().strip()
        metrics_str = json.dumps(metrics or {}, ensure_ascii=False)
        clamped_imp = max(1, min(5, int(importance)))

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO kaizen_lessons (
                    id, department, campaign_or_task, action_taken, outcome_status,
                    metrics_json, extracted_rule, importance, applied_to_departments, created_at_utc
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    lesson_id,
                    department,
                    campaign_or_task,
                    action_taken,
                    status_clean,
                    metrics_str,
                    extracted_rule,
                    clamped_imp,
                    applied_to_departments,
                    now_iso,
                ),
            )

        # Auto-promote into Tier 1 FTS5 memory so keyword searches immediately surface this lesson
        self.save_memory(
            category="KaizenLesson",
            key=f"kaizen_{department}_{campaign_or_task[:30].replace(' ', '_')}",
            content=f"[{status_clean}] ({department}) Khi làm '{campaign_or_task}': {action_taken} => BÀI HỌC KAIZEN: {extracted_rule} | Metrics: {metrics_str}",
            importance=clamped_imp,
            department=applied_to_departments,
            tags=f"kaizen,{status_clean.lower()},{department}",
        )

        return {
            "lesson_id": lesson_id,
            "department": department,
            "campaign_or_task": campaign_or_task,
            "outcome_status": status_clean,
            "extracted_rule": extracted_rule,
            "metrics": metrics or {},
            "applied_to_departments": applied_to_departments,
            "created_at_utc": now_iso,
        }

    def get_kaizen_lessons(
        self,
        department: str | None = None,
        outcome_status: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Retrieves Kaizen self-learning rules filtered by department or outcome status."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM kaizen_lessons
                WHERE (? IS NULL OR department = ? OR applied_to_departments = 'all' OR applied_to_departments LIKE '%' || ? || '%')
                  AND (? IS NULL OR outcome_status = ?)
                ORDER BY importance DESC, created_at_utc DESC
                LIMIT ?;
                """,
                (
                    department,
                    department,
                    department or "",
                    outcome_status.upper() if outcome_status else None,
                    outcome_status.upper() if outcome_status else None,
                    limit,
                ),
            ).fetchall()

        return [
            {
                "lesson_id": r["id"],
                "department": r["department"],
                "campaign_or_task": r["campaign_or_task"],
                "action_taken": r["action_taken"],
                "outcome_status": r["outcome_status"],
                "metrics": json.loads(r["metrics_json"] or "{}"),
                "extracted_rule": r["extracted_rule"],
                "importance": r["importance"],
                "applied_to_departments": r["applied_to_departments"],
                "created_at_utc": r["created_at_utc"],
            }
            for r in rows
        ]

    # =========================================================================
    # TIER 3: KNOWLEDGE GRAPH & ENTITY RAG (LightRAG + NetworkX)
    # =========================================================================
    def upsert_entity(
        self,
        name: str,
        entity_type: str,
        description: str,
        attributes: dict[str, Any] | None = None,
        department: str = "all",
    ) -> dict[str, Any]:
        """Adds or updates an Entity in the Tier 3 Corporate Knowledge Graph."""
        entity_id = f"ent_{_strip_accents(entity_type)}_{_strip_accents(name).replace(' ', '_')}"
        now_iso = _utc_now_iso()
        attr_str = json.dumps(attributes or {}, ensure_ascii=False)

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO kg_entities (entity_id, name, entity_type, description, attributes_json, department, updated_at_utc)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(entity_id) DO UPDATE SET
                    name = excluded.name,
                    description = excluded.description,
                    attributes_json = excluded.attributes_json,
                    department = excluded.department,
                    updated_at_utc = excluded.updated_at_utc;
                """,
                (entity_id, name.strip(), entity_type.strip(), description.strip(), attr_str, department, now_iso),
            )

        self.save_memory(
            category="EntityGraph",
            key=entity_id,
            content=f"[{entity_type}] {name}: {description} | Attributes: {attr_str}",
            importance=4,
            department=department,
            tags=f"entity,{entity_type.lower()}",
        )

        return {
            "entity_id": entity_id,
            "name": name.strip(),
            "entity_type": entity_type.strip(),
            "description": description.strip(),
            "attributes": attributes or {},
            "department": department,
        }

    def link_entities(
        self,
        source_name: str,
        source_type: str,
        relation_type: str,
        target_name: str,
        target_type: str,
        evidence: str = "",
        weight: float = 1.0,
    ) -> dict[str, Any]:
        """Creates a directed semantic relationship between two entities in the Knowledge Graph."""
        src_id = f"ent_{_strip_accents(source_type)}_{_strip_accents(source_name).replace(' ', '_')}"
        tgt_id = f"ent_{_strip_accents(target_type)}_{_strip_accents(target_name).replace(' ', '_')}"
        rel_id = f"rel_{uuid.uuid4().hex[:12]}"
        now_iso = _utc_now_iso()

        with self._connect() as conn:
            # Ensure nodes exist minimally if linked before explicit creation
            for eid, ename, etype in [(src_id, source_name, source_type), (tgt_id, target_name, target_type)]:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO kg_entities (entity_id, name, entity_type, description, attributes_json, department, updated_at_utc)
                    VALUES (?, ?, ?, ?, '{}', 'all', ?);
                    """,
                    (eid, ename.strip(), etype.strip(), f"Auto-created {etype} entity", now_iso),
                )

            conn.execute(
                """
                INSERT INTO kg_relations (relation_id, source_id, target_id, relation_type, weight, evidence, updated_at_utc)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_id, target_id, relation_type) DO UPDATE SET
                    weight = excluded.weight,
                    evidence = excluded.evidence,
                    updated_at_utc = excluded.updated_at_utc;
                """,
                (rel_id, src_id, tgt_id, relation_type.upper().strip(), float(weight), evidence.strip(), now_iso),
            )

        return {
            "source_id": src_id,
            "relation_type": relation_type.upper().strip(),
            "target_id": tgt_id,
            "evidence": evidence,
            "weight": weight,
        }

    def query_knowledge_graph(self, query_term: str, max_hops: int = 2) -> dict[str, Any]:
        """
        Builds a NetworkX MultiDiGraph from Tier 3 storage and performs multi-hop
        subgraph extraction around matching entities for SEO/AIO/SAO & Creative context.
        """
        G = nx.DiGraph()
        with self._connect() as conn:
            entities = conn.execute("SELECT * FROM kg_entities;").fetchall()
            relations = conn.execute("SELECT * FROM kg_relations;").fetchall()

        for e in entities:
            G.add_node(
                e["entity_id"],
                name=e["name"],
                entity_type=e["entity_type"],
                description=e["description"],
                attributes=json.loads(e["attributes_json"] or "{}"),
            )

        for r in relations:
            G.add_edge(
                r["source_id"],
                r["target_id"],
                relation_type=r["relation_type"],
                weight=r["weight"],
                evidence=r["evidence"],
            )

        norm_q = _strip_accents(query_term)
        seed_nodes = [
            nid
            for nid, data in G.nodes(data=True)
            if norm_q in _strip_accents(data.get("name", ""))
            or norm_q in _strip_accents(data.get("description", ""))
            or norm_q in _strip_accents(data.get("entity_type", ""))
        ]

        visited: set[str] = set(seed_nodes)
        frontier: set[str] = set(seed_nodes)
        for _ in range(max(1, max_hops)):
            next_frontier: set[str] = set()
            for node in frontier:
                neighbors = set(G.successors(node)) | set(G.predecessors(node))
                next_frontier.update(neighbors - visited)
            visited.update(next_frontier)
            frontier = next_frontier

        subG = G.subgraph(visited)
        nodes_out = [
            {"entity_id": nid, **data}
            for nid, data in subG.nodes(data=True)
        ]
        edges_out = [
            {
                "source": u,
                "source_name": G.nodes[u].get("name", u),
                "relation_type": edata.get("relation_type", "RELATED_TO"),
                "target": v,
                "target_name": G.nodes[v].get("name", v),
                "evidence": edata.get("evidence", ""),
                "weight": edata.get("weight", 1.0),
            }
            for u, v, edata in subG.edges(data=True)
        ]

        return {
            "query": query_term,
            "matched_seed_entities": len(seed_nodes),
            "subgraph_nodes": nodes_out,
            "subgraph_relations": edges_out,
        }

    # =========================================================================
    # FINANCIAL & ROI LEDGER (For CFO #13 & Accountant #14)
    # =========================================================================
    def record_financial_transaction(
        self,
        department: str,
        campaign_id: str,
        tx_type: str,
        amount_vnd: float,
        leads_count: int = 0,
        orders_count: int = 0,
        note: str = "",
    ) -> dict[str, Any]:
        tx_id = f"tx_{uuid.uuid4().hex[:12]}"
        now_iso = _utc_now_iso()
        clean_type = tx_type.upper().strip()

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO finance_ledger (tx_id, department, campaign_id, tx_type, amount_vnd, leads_count, orders_count, note, created_at_utc)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (tx_id, department, campaign_id, clean_type, float(amount_vnd), int(leads_count), int(orders_count), note, now_iso),
            )

        return {
            "tx_id": tx_id,
            "department": department,
            "campaign_id": campaign_id,
            "tx_type": clean_type,
            "amount_vnd": amount_vnd,
            "leads_count": leads_count,
            "orders_count": orders_count,
            "created_at_utc": now_iso,
        }

    def get_financial_summary(self, campaign_id: str | None = None) -> dict[str, Any]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT tx_type, SUM(amount_vnd) AS total_vnd, SUM(leads_count) AS total_leads, SUM(orders_count) AS total_orders
                FROM finance_ledger
                WHERE (? IS NULL OR campaign_id = ?)
                GROUP BY tx_type;
                """,
                (campaign_id, campaign_id),
            ).fetchall()

        totals: dict[str, float] = {}
        leads = 0
        orders = 0
        for r in rows:
            totals[r["tx_type"]] = float(r["total_vnd"] or 0.0)
            leads += int(r["total_leads"] or 0)
            orders += int(r["total_orders"] or 0)

        revenue = totals.get("REVENUE", 0.0)
        spend = (
            totals.get("AD_SPEND", 0.0)
            + totals.get("PROXY_COST", 0.0)
            + totals.get("TOOL_COST", 0.0)
            + totals.get("REFUND", 0.0)
        )
        profit = revenue - spend
        roas = round(revenue / spend, 2) if spend > 0 else 0.0
        cpl = round(spend / leads, 0) if leads > 0 else 0.0

        return {
            "campaign_id": campaign_id or "ALL_COMPANY",
            "revenue_vnd": revenue,
            "total_cost_vnd": spend,
            "net_profit_vnd": profit,
            "roas": roas,
            "total_leads": leads,
            "total_orders": orders,
            "cost_per_lead_vnd": cpl,
            "breakdown": totals,
        }

    # =========================================================================
    # UNIFIED DEPARTMENT CONTEXT BRIEFING (Combines Tiers 1 + 2 + 3)
    # =========================================================================
    def build_department_context_briefing(
        self,
        department_id: str,
        topic_or_product: str | None = None,
    ) -> dict[str, Any]:
        """
        Generates a complete operational briefing for any of the 16 AI departments by
        combining:
        - Department SOP & Weapons (Tier 1)
        - Relevant Product/Brand Memories (Tier 1 BM25)
        - Kaizen Winning & Losing Lessons (Tier 2 Episodic)
        - Multi-hop Entity Knowledge Graph (Tier 3 LightRAG/NetworkX)
        - Live CFO ROAS Snapshot
        """
        dept_meta = CORPORATE_DEPARTMENTS.get(department_id, {
            "name": department_id,
            "role": "Chuyên viên AI",
            "weapons": "CorporateSecondBrain",
        })

        memories = self.query_memories(
            keyword=topic_or_product,
            department=department_id,
            limit=15,
        )
        kaizen_rules = self.get_kaizen_lessons(department=department_id, limit=10)
        graph_context = (
            self.query_knowledge_graph(topic_or_product, max_hops=2)
            if topic_or_product
            else {"subgraph_nodes": [], "subgraph_relations": []}
        )
        finance = self.get_financial_summary()

        return {
            "department_id": department_id,
            "department_meta": dept_meta,
            "topic_focus": topic_or_product or "general",
            "tier1_memories": memories,
            "tier2_kaizen_lessons": kaizen_rules,
            "tier3_knowledge_graph": graph_context,
            "cfo_financial_snapshot": finance,
        }
