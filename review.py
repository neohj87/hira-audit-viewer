import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import os

# ==============================================================================
# 1. 마스터 스키마 정의
# ==============================================================================
SCHEMA_H = {
    "sender_id": (1, 6, 0, "송신자ID"), "claim_id": (7, 10, 0, "청구번호"), "record_type": (17, 1, 0, "내역구분"),
    "format_div": (18, 3, 0, "서식구분"), "hospital_code": (21, 8, 0, "요양기관기호"), "receiver": (29, 1, 0, "수신기관"),
    "insure_type": (30, 1, 0, "보험자종별구분"), "claim_type": (31, 1, 0, "청구구분"), "claim_unit": (32, 1, 0, "청구단위구분"),
    "treat_div": (33, 1, 0, "진료구분"), "treat_field": (34, 1, 0, "진료분야구분"), "treat_type": (35, 1, 0, "진료형태"),
    "treat_year_month": (36, 6, 0, "진료년월"), "total_claim_cnt": (42, 6, 0, "건수"), "total_amt_1": (48, 12, 0, "요양급여비용총액1"),
    "patient_amt": (60, 12, 0, "본인일부부담금"), "upper_limit_excess": (72, 12, 0, "본인부담상한액초과금"),
    "claim_amt": (84, 12, 0, "청구액"), "support_amt": (96, 12, 0, "지원금"), "handicap_amt": (108, 12, 0, "장애인의료비"),
    "total_amt_2": (120, 12, 0, "요양급여비용총액2"), "bohun_claim_amt": (132, 12, 0, "보훈청구액"),
    "full_patient_amt": (144, 12, 0, "100/100본인부담금"), "bohun_patient_amt": (156, 12, 0, "보훈본인일부부담금"),
    "under_100_total_amt": (168, 12, 0, "100/100미만총액"), "under_100_patient_amt": (180, 12, 0, "100/100미만본인부담"),
    "under_100_claim_amt": (192, 12, 0, "100/100미만청구액"), "under_100_bohun_amt": (204, 12, 0, "100/100미만보훈청구"),
    "diff_apply_days": (216, 6, 2, "차등수가적용일수"), "doctor_cnt": (222, 4, 2, "의사수"), "diff_index": (226, 8, 7, "차등지수"),
    "diff_claim_amt": (234, 12, 0, "차등수가청구액"), "claim_date": (246, 8, 0, "청구일자"), "claim_person": (254, 20, 0, "청구인"),
    "writer_name": (274, 20, 0, "작성자성명"), "writer_ssn": (294, 13, 0, "작성자생년월일"), "approval_no": (307, 35, 0, "검사승인번호"),
    "agency_code": (342, 5, 0, "대행청구단체기호")
}

SCHEMA_A = {
    "claim_id": (1, 10, 0, "청구번호"), "serial_no": (11, 5, 0, "명세서일련번호"), "record_type": (16, 1, 0, "내역구분"),
    "form_no": (17, 4, 0, "서식번호"), "hospital_code": (21, 8, 0, "요양기관기호"), "guarantee_org_code": (29, 11, 0, "보장기관기호"),
    "medical_care_type": (40, 1, 0, "의료급여종별구분"), "official_injury_type": (41, 1, 0, "공상등구분"),
    "fixed_rate_div": (42, 1, 0, "정액_정률구분"), "claim_type_div": (43, 1, 0, "청구구분"), "orig_receipt_no": (44, 7, 0, "접수번호"),
    "orig_serial_no": (51, 5, 0, "당초_명세서일련번호"), "return_reason_code": (56, 2, 0, "사유코드"),
    "first_admit_date": (58, 8, 0, "최초입원개시일"), "subscriber_name": (66, 20, 0, "가입자성명"),
    "insurance_cert_no": (86, 20, 0, "증번호"), "patient_name": (106, 20, 0, "수진자성명"),
    "patient_ssn": (126, 13, 0, "수진자주민등록번호"), "care_days": (139, 3, 0, "요양급여일수"), "visit_days": (142, 3, 0, "입원_총내원일수"),
    "empty_space_1": (145, 31, 0, "공란1"), "admit_route": (176, 2, 0, "입원경로"), "treat_result": (178, 1, 0, "진료결과"),
    "total_amt_1": (179, 10, 0, "요양급여비용총액1"), "patient_amt": (189, 10, 0, "본인일부부담금"),
    "upper_limit_excess": (199, 10, 0, "본인부담상한액초과금"), "claim_amt": (209, 10, 0, "청구액"),
    "support_amt": (219, 10, 0, "지원금"), "handicap_amt": (229, 10, 0, "장애인의료비"), "loan_amt": (239, 10, 0, "대불금"),
    "total_amt_2": (249, 10, 0, "요양급여비용총액2"), "bohun_claim_amt": (259, 10, 0, "보훈청구액"),
    "empty_space_2": (269, 10, 0, "공란2"), "empty_space_3": (279, 10, 0, "공란3"), "full_patient_amt": (289, 10, 0, "100/100본인부담총액"),
    "bohun_patient_amt": (299, 10, 0, "보훈본인일부부담금"), "under_100_total_amt": (309, 10, 0, "100/100미만총액"),
    "under_100_patient_amt": (319, 10, 0, "100/100미만본인부담"), "under_100_claim_amt": (329, 10, 0, "100/100미만청구액"),
    "under_100_bohun_amt": (339, 10, 0, "100/100미만보훈청구")
}

SCHEMA_B = {
    "claim_id": (1, 10, 0, "청구번호"), "serial_no": (11, 5, 0, "명세서일련번호"), "record_type": (16, 1, 0, "내역구분"),
    "sick_type_div": (17, 1, 0, "상병분류구분"), "sick_code": (18, 6, 0, "상병분류기호"), "treat_dept": (24, 2, 0, "진료과목"),
    "internal_dept_dtl": (26, 2, 0, "내과세부전문과목"), "treat_start_date": (28, 8, 0, "내원일자_당월요양개시일"),
    "doc_license_type": (36, 1, 0, "면허종류"), "doc_license_no": (37, 10, 0, "면허번호"), "tooth_ur": (47, 8, 0, "우상치식"),
    "tooth_ul": (55, 8, 0, "좌상치식"), "tooth_lr": (63, 8, 0, "우하치식"), "tooth_ll": (71, 8, 0, "좌하치식")
}

SCHEMA_C = {
    "claim_id": (1, 10, 0, "청구번호"), "serial_no": (11, 5, 0, "명세서일련번호"), "record_type": (16, 1, 0, "내역구분"),
    "category": (17, 2, 0, "항"), "sub_category": (19, 2, 0, "목"), "line_no": (21, 4, 0, "줄번호"),
    "code_div": (25, 1, 0, "코드구분"), "treat_code": (26, 9, 0, "코드"), "unit_price": (35, 12, 2, "단가"),
    "day_dose": (47, 7, 2, "1일투여량"), "total_days": (54, 3, 0, "총투여일수"), "dose_per_once": (57, 9, 4, "1회투약량"),
    "amount": (66, 10, 0, "금액"), "empty_1": (76, 10, 0, "공란1"), "empty_2": (86, 10, 0, "공란2"),
    "mod_date": (96, 8, 0, "변경일"), "doc_license_type": (104, 1, 0, "면허종류"), "doc_license_no": (105, 100, 0, "면허번호"),
    "tooth_ur": (205, 8, 0, "우상치식"), "tooth_ul": (213, 8, 0, "좌상치식"), "tooth_lr": (221, 8, 0, "우하치식"),
    "tooth_ll": (229, 6, 0, "좌하치식")
}

SCHEMA_D = {
    "claim_id": (1, 10, 0, "청구번호"), "serial_no": (11, 5, 0, "명세서일련번호"), "record_type": (16, 1, 0, "내역구분"),
    "presc_issue_no": (17, 13, 0, "처방전발급번호"), "presc_days": (30, 3, 0, "처방일수"), "repeat_cnt": (33, 2, 0, "반복조제횟수"),
    "line_no": (35, 4, 0, "줄번호"), "code_div": (39, 1, 0, "코드구분"), "medi_code": (40, 9, 0, "코드"),
    "dose_per_once": (49, 9, 4, "1회투약량"), "dose_per_day": (58, 2, 0, "1일투여횟수"), "total_presc_days": (60, 3, 0, "총투약일수"),
    "copay_type": (63, 1, 0, "본인부담률구분코드")
}

SCHEMA_E = {
    "claim_id": (1, 10, 0, "청구번호"), "serial_no": (11, 5, 0, "명세서일련번호"), "record_type": (16, 1, 0, "내역구분"),
    "occur_unit_div": (17, 1, 0, "발생단위구분"), "presc_issue_no": (18, 13, 0, "처방전발급번호"), "line_no": (31, 4, 0, "줄번호"),
    "spec_code": (35, 5, 0, "특정내역구분"), "spec_detail": (40, 700, 0, "특정내역")
}

SCHEMAS = {'H': SCHEMA_H, 'A': SCHEMA_A, 'B': SCHEMA_B, 'C': SCHEMA_C, 'D': SCHEMA_D, 'E': SCHEMA_E}

# ==============================================================================
# UI 디스플레이 컬럼
# ==============================================================================
DISPLAY_COLUMNS = {
    'A': ["serial_no", "medical_care_type", "first_admit_date", "patient_name", "patient_ssn", "care_days", "patient_amt", "total_amt_1", "claim_amt"],
    'B': ["sick_type_div", "sick_code", "treat_dept", "treat_start_date", "doc_license_no"],
    'C': ["category", "line_no", "code_div", "treat_code", "unit_price", "day_dose", "total_days", "amount"],
    'D': ["presc_issue_no", "line_no", "code_div", "medi_code", "dose_per_once", "total_presc_days"],
    'E': ["line_no", "spec_code", "spec_detail"]
}

# ==============================================================================
# 모듈 레벨 상수 (FIX v2.9: 루프 밖으로 이동)
# ==============================================================================
REQUIRED_RULES = {
    "652601250": ["B373"],
    "671800840": ["B373"]
}

TWIN_TARGET_CODES = [
    "EB511", "EB512", "EB513", "EB514", "EB515", "EB517", "EB518", "E7326"
]

# 고시 제2019-166호 기준 임산부 초음파 코드 분류
# ※ 일반/정밀은 별개 카운팅 — 절대 합산하지 않음
# (접두어 매칭 사용 — EB511이 EB511001·EB511010·EB511011 등을 포함)

# [1삼분기] 일반 (나951가(1)) — 0~13주, 2회 기본급여, 3회부터 JX999
EARLY_US_CODES = ["EB511", "EB512"]

# [1삼분기] 정밀 (나951가(2)) — 11~13주, 1회 기본급여, 2회부터 JX999
FIRST_TRI_DETAIL_CODES = ["EB513", "EB514"]

# [2,3삼분기] 일반 (나951나(1)) — 각 구간 1회 기본급여, 2회부터 JX999
SECOND_THIRD_GENERAL_CODES = ["EB515", "EB516"]

# [2,3삼분기] 정밀 (나951나(2)) — 1회 기본급여, 2회부터 JX999
SECOND_THIRD_DETAIL_CODES = ["EB517", "EB518"]

# 조건 9용: 14주 미만인데 사용하면 코드오류인 코드 (2,3삼분기 전체)
SECOND_THIRD_US_CODES = SECOND_THIRD_GENERAL_CODES + SECOND_THIRD_DETAIL_CODES

# 조건 8 그룹 B용 통합 참조 (실제 심사는 그룹별 독립 카운팅)
OTHER_OB_US_CODES = FIRST_TRI_DETAIL_CODES + SECOND_THIRD_GENERAL_CODES + SECOND_THIRD_DETAIL_CODES


# ==============================================================================
# 유틸 함수
# ==============================================================================
def safe_float(val_str: str) -> float:
    """쉼표가 포함된 포맷 문자열을 안전하게 float으로 변환 (FIX v2.9)"""
    try:
        return float(str(val_str).replace(',', ''))
    except (ValueError, TypeError):
        return 0.0


def parse_jt005_week(e_rows: list) -> int | None:
    """E레코드에서 JT005 특정내역을 찾아 임신 주수(정수)를 반환. 실패 시 None.
    지원 형식: '13+6'(주+일), '13'(주만), '130'(13주0일 3자리) 등
    """
    for e in e_rows:
        if e.get('spec_code', '').strip().upper() == 'JT005':
            detail = e.get('spec_detail', '').strip()
            # "13+6", "13+0" 형식 (가장 일반적)
            if '+' in detail:
                try:
                    return int(detail.split('+')[0].strip())
                except ValueError:
                    pass
            # 숫자만 있는 경우 ("13", "14")  또는 3자리("130" = 13주0일)
            digits = ''.join(c for c in detail if c.isdigit())
            if digits:
                try:
                    val = int(digits[:3])
                    return val // 10 if val >= 100 else val
                except ValueError:
                    pass
    return None


def calc_age(patient_ssn: str) -> int | None:
    """주민등록번호 앞 7자리로 만 나이 계산. 실패 시 None 반환"""
    if len(patient_ssn) < 7:
        return None
    gender_code = patient_ssn[6]
    if gender_code in ('1', '2', '5', '6'):
        prefix = "19"
    elif gender_code in ('3', '4', '7', '8'):
        prefix = "20"
    else:
        prefix = "19"
    try:
        birth = datetime.strptime(prefix + patient_ssn[:6], "%Y%m%d")
        today = datetime.now()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    except ValueError:
        return None


# ==============================================================================
# 메인 어플리케이션
# ==============================================================================
class SinglePageReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("심평원 청구데이터 사전심사 시스템 v3.0")
        self.root.geometry("1450x950")

        self.h_record = {}
        self.patients_db = {}
        self.patient_ssn_index = {}   # v3.0 신규: 주민번호 → 명세서 목록 인덱스
        self.audit_run = False

        self._build_ui()

    # --------------------------------------------------------------------------
    # UI 구성
    # --------------------------------------------------------------------------
    def _build_ui(self):
        top_frame = tk.Frame(self.root, bg="#2C5282", pady=10, padx=10)
        top_frame.pack(fill=tk.X)
        tk.Label(top_frame, text="🏥 HIRA 통합 사전심사 뷰어", fg="white", bg="#2C5282",
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)

        tk.Button(top_frame, text="🚨 사전심사 실행", font=("Arial", 10, "bold"),
                  bg="#E53E3E", fg="white", command=self.run_audit).pack(side=tk.RIGHT, padx=5)
        tk.Button(top_frame, text="📂 EDI 청구파일(.B02) 불러오기", font=("Arial", 10, "bold"),
                  command=self.load_file).pack(side=tk.RIGHT, padx=5)

        main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ── 좌측: 환자 목록 ──
        left_frame = ttk.LabelFrame(main_pane, text=" 수진자 목록 ")
        main_pane.add(left_frame, weight=1)

        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=15)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        search_entry.insert(0, "코드 검색...")

        def on_entry_click(event):
            if self.search_var.get() == "코드 검색...":
                search_entry.delete(0, "end")

        def on_focusout(event):
            if self.search_var.get() == "":
                search_entry.insert(0, "코드 검색...")

        search_entry.bind('<FocusIn>', on_entry_click)
        search_entry.bind('<FocusOut>', on_focusout)
        search_entry.bind("<Return>", lambda e: self.search_patients())

        ttk.Button(search_frame, text="검색", command=self.search_patients, width=4).pack(side=tk.LEFT, padx=1)
        ttk.Button(search_frame, text="초기화", command=self.reset_search, width=5).pack(side=tk.LEFT)

        tree_container = ttk.Frame(left_frame)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=0)

        style = ttk.Style()
        style.map("Treeview",
                  foreground=self.fixed_map("foreground"),
                  background=self.fixed_map("background"))

        self.tree_patients = ttk.Treeview(tree_container,
                                          columns=("id", "name", "status"),
                                          show="headings")
        self.tree_patients.heading("id",     text="명일련",  command=lambda c="id":     self.sort_tree(self.tree_patients, c, False))
        self.tree_patients.heading("name",   text="수진자명", command=lambda c="name":   self.sort_tree(self.tree_patients, c, False))
        self.tree_patients.heading("status", text="확인필요", command=lambda c="status": self.sort_tree(self.tree_patients, c, True))
        self.tree_patients.column("id",     width=50,  anchor="center")
        self.tree_patients.column("name",   width=70,  anchor="center")
        self.tree_patients.column("status", width=60,  anchor="center")
        self.tree_patients.bind("<<TreeviewSelect>>", self.on_patient_select)

        vsb_patients = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree_patients.yview)
        self.tree_patients.configure(yscrollcommand=vsb_patients.set)
        self.tree_patients.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb_patients.pack(side=tk.RIGHT, fill=tk.Y)

        self.lbl_patient_count = tk.Label(left_frame, text="전체: 0명 / 조회: 0명",
                                          fg="#2C5282", font=("Arial", 10, "bold"),
                                          bg="#e2e8f0", pady=3)
        self.lbl_patient_count.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # ── 우측: 통합 스크롤 영역 ──
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=5)

        canvas = tk.Canvas(right_frame)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        right_frame.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.trees = {}
        sections = [
            ("A",     "명세서 일반내역 (A)",              1),
            ("B",     "상병내역 (B)",                     3),
            ("C",     "진료내역 (C)",                     6),
            ("D",     "처방내역 (D)",                     3),
            ("E",     "특정내역기재란 (E)",                3),
            ("AUDIT", "🚨 사전심사 결과 (선택된 환자 기준)", 4),
        ]

        for key, title, h_lines in sections:
            lf = ttk.LabelFrame(self.scrollable_frame, text=f" {title} ")
            lf.pack(fill=tk.X, expand=True, padx=5, pady=10)

            if key == "AUDIT":
                cols = ("id", "type", "code", "msg")
                tree = ttk.Treeview(lf, columns=cols, show="headings", height=h_lines)
                tree.heading("id",   text="명일련")
                tree.heading("type", text="심사유형")
                tree.heading("code", text="관련코드")
                tree.heading("msg",  text="심사/조정 메시지")
                tree.column("id",   width=60,  anchor="center")
                tree.column("type", width=100, anchor="center")
                tree.column("code", width=100, anchor="center")
                tree.column("msg",  width=500, anchor="w")
            else:
                schema       = SCHEMAS[key]
                display_cols = DISPLAY_COLUMNS[key]
                tree = ttk.Treeview(lf, columns=display_cols, show="headings", height=h_lines)
                for c in display_cols:
                    kor_name = schema[c][3]
                    tree.heading(c, text=kor_name)
                    w = 400 if c == "spec_detail" else 100
                    tree.column(c, width=w,
                                anchor="center" if "name" not in c and "detail" not in c else "w")

            vsb = ttk.Scrollbar(lf, orient="vertical",   command=tree.yview)
            hsb = ttk.Scrollbar(lf, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

            tree.grid(row=0, column=0, sticky='nsew')
            vsb.grid(row=0, column=1, sticky='ns')
            hsb.grid(row=1, column=0, sticky='ew')

            lf.grid_columnconfigure(0, weight=1)
            lf.grid_rowconfigure(0, weight=1)

            self.trees[key] = tree

    # --------------------------------------------------------------------------
    # 헬퍼
    # --------------------------------------------------------------------------
    def fixed_map(self, option):
        return [elm for elm in ttk.Style().map("Treeview", query_opt=option)
                if elm[:2] != ("!disabled", "!selected")]

    def sort_tree(self, tree, col, reverse):
        items = [(tree.set(k, col), k) for k in tree.get_children('')]
        items.sort(reverse=reverse)
        for index, (_, k) in enumerate(items):
            tree.move(k, '', index)
        tree.heading(col, command=lambda: self.sort_tree(tree, col, not reverse))

    # --------------------------------------------------------------------------
    # 환자 목록 갱신 / 검색
    # --------------------------------------------------------------------------
    def refresh_patient_list(self, search_keyword=""):
        for item in self.tree_patients.get_children():
            self.tree_patients.delete(item)

        keyword = search_keyword.strip().upper()
        if keyword == "코드 검색...":
            keyword = ""

        total_patients = len(self.patients_db)
        filtered_count = 0

        for p_id, data in self.patients_db.items():
            if keyword:
                found = (
                    any(keyword in b.get('sick_code',  '').upper() for b in data['B']) or
                    any(keyword in c.get('treat_code', '').upper() for c in data['C'])
                )
                if not found:
                    continue

            status_mark = "❗" if data.get('AUDIT') else ""
            self.tree_patients.insert("", "end", values=(p_id, data["name"], status_mark))
            filtered_count += 1

        self.lbl_patient_count.config(text=f"전체: {total_patients}명 / 조회: {filtered_count}명")

    def search_patients(self):
        if not self.patients_db:
            return
        self.refresh_patient_list(self.search_var.get())

    def reset_search(self):
        if not self.patients_db:
            return
        self.search_var.set("코드 검색...")
        self.refresh_patient_list("")

    # --------------------------------------------------------------------------
    # 파싱 엔진
    # --------------------------------------------------------------------------
    def parse_bytes_line(self, b_line: bytes, schema: dict, rec_type: str) -> dict:
        max_len = max(pos + length - 1 for pos, length, _, _ in schema.values())
        if len(b_line) < max_len:
            b_line = b_line.ljust(max_len, b' ')

        parsed_data = {}
        for var_name, (pos, length, dec, kor_name) in schema.items():
            chunk   = b_line[pos - 1: pos - 1 + length]
            val_str = chunk.decode('cp949', errors='ignore').strip()

            is_number = dec >= 0 and any(
                kw in kor_name for kw in ["금액", "일수", "횟수", "건수", "의사수", "량", "단가", "지수", "총액", "의료비", "대불금"]
            )
            is_except = any(
                kw in kor_name for kw in ["번호", "기호", "코드", "구분", "ID", "일련", "성명", "기관", "경로", "결과"]
            )

            if is_number and not is_except:
                try:
                    num = float(val_str) if val_str else 0.0

                    if rec_type == 'C':
                        if var_name == "unit_price":   num /= 10000
                        elif var_name == "amount":     num /= 100
                        elif var_name == "day_dose":   num /= 10000
                        elif var_name == "total_days": num /= 100
                    elif rec_type == 'D':
                        if var_name == "dose_per_once": num /= 10000

                    parsed_data[var_name] = f"{int(num):,}" if float(num).is_integer() else f"{num:,.{dec}f}"
                except ValueError:
                    parsed_data[var_name] = "0"
            else:
                # v3.0: patient_ssn — UI 표시용(마스킹) + 인덱스용 원본 동시 저장
                if var_name == "patient_ssn" and len(val_str) == 13:
                    parsed_data["patient_ssn"]     = val_str[:6] + "-*******"  # UI 표시
                    parsed_data["patient_ssn_raw"] = val_str                    # 인덱스용 원본
                else:
                    parsed_data[var_name] = val_str

        return parsed_data

    # --------------------------------------------------------------------------
    # 파일 로드
    # --------------------------------------------------------------------------
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("EDI Files", "*.B02")])
        if not file_path:
            return

        self.h_record          = {}
        self.patients_db       = {}
        self.patient_ssn_index = {}   # v3.0: 인덱스 초기화
        self.audit_run         = False

        with open(file_path, 'rb') as f:
            for raw_line in f:
                b_line = raw_line.replace(b'\xef\xbb\xbf', b'').replace(b'\r', b'').replace(b'\n', b'')
                if len(b_line) < 15:
                    continue

                if b_line.startswith(b"090") or b_line.startswith(b"092"):
                    rec_type = 'H'
                else:
                    rec_type = b_line[15:16].decode('cp949', errors='ignore')

                if rec_type not in SCHEMAS:
                    continue

                parsed = self.parse_bytes_line(b_line, SCHEMAS[rec_type], rec_type)

                if rec_type == 'H':
                    self.h_record = parsed
                else:
                    p_id = parsed.get("serial_no", "")
                    if not p_id:
                        continue
                    if p_id not in self.patients_db:
                        self.patients_db[p_id] = {
                            "name": "", "A": [], "B": [], "C": [], "D": [], "E": [], "AUDIT": []
                        }
                    if rec_type == 'A':
                        name_val = parsed.get("patient_name", "").strip()
                        self.patients_db[p_id]["name"] = name_val if name_val else "이름없음"
                    self.patients_db[p_id][rec_type].append(parsed)

        # v3.0: 파일 로드 완료 후 주민번호 기준 인덱스 생성
        for serial_no, data in self.patients_db.items():
            for a_row in data.get('A', []):
                ssn_raw = a_row.get('patient_ssn_raw', '')
                if ssn_raw:
                    if ssn_raw not in self.patient_ssn_index:
                        self.patient_ssn_index[ssn_raw] = []
                    if serial_no not in self.patient_ssn_index[ssn_raw]:
                        self.patient_ssn_index[ssn_raw].append(serial_no)

        self.search_var.set("코드 검색...")
        self.refresh_patient_list("")

        for t in ['A', 'B', 'C', 'D', 'E', 'AUDIT']:
            for item in self.trees[t].get_children():
                self.trees[t].delete(item)

        messagebox.showinfo("로드 완료", f"파일 파싱 성공!\n총 환자: {len(self.patients_db)}명")

    # --------------------------------------------------------------------------
    # 환자 선택
    # --------------------------------------------------------------------------
    def on_patient_select(self, event):
        sel = self.tree_patients.selection()
        if not sel:
            return
        p_id = self.tree_patients.item(sel[0], "values")[0]
        data = self.patients_db[p_id]

        for t in ['A', 'B', 'C', 'D', 'E']:
            tree = self.trees[t]
            for item in tree.get_children():
                tree.delete(item)
            for row_dict in data[t]:
                vals = [row_dict.get(c, "") for c in DISPLAY_COLUMNS[t]]
                tree.insert("", "end", values=vals)

        tree_audit = self.trees['AUDIT']
        for item in tree_audit.get_children():
            tree_audit.delete(item)

        if not self.audit_run:
            tree_audit.insert("", "end", values=(p_id, "안내", "-", "상단의 [사전심사 실행] 버튼을 눌러주세요."))
        elif not data['AUDIT']:
            tree_audit.insert("", "end", values=(p_id, "심사통과", "-", "발견된 삭감/조정 위험이 없습니다. 청구 가능!"))
        else:
            for res in data['AUDIT']:
                tree_audit.insert("", "end", values=res)

    # --------------------------------------------------------------------------
    # 사전심사 로직
    # --------------------------------------------------------------------------
    def run_audit(self):
        if not self.patients_db:
            messagebox.showwarning("경고", "먼저 청구 파일을 불러와주세요.")
            return

        self.audit_run   = True
        problematic_pids = set()
        total_errors     = 0

        # ======================================================================
        # 명세서 단위 심사 (기존 조건 1~7 — 변경 없음)
        # ======================================================================
        for p_id, data in self.patients_db.items():
            data['AUDIT'] = []
            c_rows = data.get('C', [])
            if not c_rows:
                continue

            # ── 심사조건 1: EB455 JX999 누락 ──────────────────────────────
            if any("EB455" in r.get('treat_code', '').upper() for r in c_rows):
                has_jx999 = any(
                    r.get('spec_code', '').strip().upper() == 'JX999'
                    for r in data.get('E', [])
                )
                if not has_jx999:
                    data['AUDIT'].append((p_id, "청구메모 미기재", "EB455",
                                          "진단초음파(EB455)가 청구되었으나, 특정내역(JX999) 메모가 누락되었습니다."))
                    problematic_pids.add(p_id); total_errors += 1

            # ── 심사조건 2: R4106 — B373 또는 N72 상병 필수 ──────────────
            if any("R4106" in r.get('treat_code', '').upper() for r in c_rows):
                has_sick = any(
                    "B373" in r.get('sick_code', '').upper() or "N72" in r.get('sick_code', '').upper()
                    for r in data.get('B', [])
                )
                if not has_sick:
                    data['AUDIT'].append((p_id, "상병누락", "R4106",
                                          "R4106 수가 청구 시 B373 또는 N72 상병코드 중 최소 하나가 필요합니다."))
                    problematic_pids.add(p_id); total_errors += 1

            # ── 심사조건 3: EB516 JX999 누락 ──────────────────────────────
            if any("EB516" in r.get('treat_code', '').upper() for r in c_rows):
                has_jx999 = any(
                    r.get('spec_code', '').strip().upper() == 'JX999'
                    for r in data.get('E', [])
                )
                if not has_jx999:
                    data['AUDIT'].append((p_id, "청구메모 미기재", "EB516",
                                          "고위험 초음파(EB516)가 청구되었으나, 특정내역(JX999) 메모가 누락되었습니다."))
                    problematic_pids.add(p_id); total_errors += 1

            # ── 심사조건 4: 다태아(O300) — 대상 수가 1.5배 청구 확인 ──────
            is_twin = any("O300" in r.get('sick_code', '').upper() for r in data.get('B', []))
            if is_twin:
                for c_row in c_rows:
                    code = c_row.get('treat_code', '').upper()
                    if any(t in code for t in TWIN_TARGET_CODES):
                        dose = safe_float(c_row.get('day_dose', '0'))
                        if dose < 1.5:
                            data['AUDIT'].append((p_id, "청구 누락(다태아)", code,
                                                  f"다태아(O300) 환자입니다. {code}는 1.5배 청구 가능하나 현재 {dose}로 청구되었습니다."))
                            problematic_pids.add(p_id); total_errors += 1

            # ── 심사조건 5: 약제-상병 매핑 ────────────────────────────────
            for d_row in data.get('D', []):
                medi_code = d_row.get('medi_code', '').strip()
                if medi_code in REQUIRED_RULES:
                    required_sicks = REQUIRED_RULES[medi_code]
                    has_required = any(
                        s in r.get('sick_code', '').upper()
                        for r in data.get('B', [])
                        for s in required_sicks
                    )
                    if not has_required:
                        data['AUDIT'].append((p_id, "상병누락(약제)", medi_code,
                                              f"약제({medi_code}) 처방 시 {required_sicks} 상병이 필수이나 누락되었습니다."))
                        problematic_pids.add(p_id); total_errors += 1

            # ── 심사조건 6: ID602 — JT041 특정내역 필수 ───────────────────
            if any("ID602" in r.get('treat_code', '').upper() for r in c_rows):
                has_jt041 = any(
                    r.get('spec_code', '').strip().upper() == 'JT041'
                    for r in data.get('E', [])
                )
                if not has_jt041:
                    data['AUDIT'].append((p_id, "청구메모 미기재", "ID602",
                                          "수가코드 ID602 청구 시 특정내역(JT041) 기재가 필수이나 누락되었습니다."))
                    problematic_pids.add(p_id); total_errors += 1

            # ── 심사조건 7: E7325 2회차 — 나이·JX999 ──────────────────────
            e7325_list = [r for r in c_rows if "E7325" in r.get('treat_code', '').upper()]
            if len(e7325_list) >= 2:
                ssn = next((r.get('patient_ssn', '') for r in data.get('A', [])), "")
                age = calc_age(ssn)
                if age is not None:
                    if age <= 35:
                        data['AUDIT'].append((p_id, "삭감주의(나이제한)", "E7325",
                                              f"만 {age}세로 2회차 청구 시 삭감 대상입니다."))
                        problematic_pids.add(p_id); total_errors += 1
                    else:
                        has_jx999 = any(
                            r.get('spec_code', '').strip().upper() == 'JX999'
                            for r in data.get('E', [])
                        )
                        if not has_jx999:
                            data['AUDIT'].append((p_id, "청구 누락(횟수초과)", "E7325",
                                                  "만 35세 초과자 2회차 청구 시 특정내역(JX999)이 필수이나 누락되었습니다."))
                            problematic_pids.add(p_id); total_errors += 1

            # ── 심사조건 9: 주수 불일치 — 14주 미만인데 2,3삼분기 코드 사용 ──
            # EB513/EB514(1삼분기 정밀)는 14주 미만에 사용이 정상이므로 제외
            # SECOND_THIRD_US_CODES(EB515~EB518)만 체크
            gestation_week = parse_jt005_week(data.get('E', []))
            if gestation_week is not None and gestation_week < 14:
                wrong_codes = list({
                    c.get('treat_code', '').upper()
                    for c in c_rows
                    if any(code in c.get('treat_code', '').upper() for code in SECOND_THIRD_US_CODES)
                })
                for wc in wrong_codes:
                    data['AUDIT'].append((
                        p_id,
                        "코드오류(주수불일치)",
                        wc,
                        f"JT005 기준 임신 {gestation_week}주 (14주 미만)이나 "
                        f"2,3삼분기 초음파 코드({wc}) 청구 — 코드 확인 필요"
                    ))
                    problematic_pids.add(p_id)
                    total_errors += 1

        # ======================================================================
        # v3.0 신규 — 심사조건 8: 동일 환자 임산부 초음파 통합 심사
        #
        # [그룹 A] EB511/EB512 (0~13주6일 구간)
        #   - 2회까지 JX999 메모 불필요
        #   - 3회째부터 JX999 필수 (주수 확인: E레코드 JT005)
        #
        # [그룹 B] EB513~EB518 (그 외)
        #   - 1회까지 JX999 메모 불필요
        #   - 2회째부터 JX999 필수
        #
        # 기준: 동일 주민번호, 같은 청구서(한 달) 내, B레코드 내원일자 날짜순
        # ======================================================================

        def get_date_str(data):
            """B레코드에서 내원일자 추출. 주상병 우선, 없으면 첫 B레코드"""
            b_rows = data.get('B', [])
            for b in b_rows:
                if b.get('sick_type_div', '') == '1':
                    return b.get('treat_start_date', '99999999')
            return b_rows[0].get('treat_start_date', '99999999') if b_rows else '99999999'

        def check_jx999(data):
            return any(
                e.get('spec_code', '').strip().upper() == 'JX999'
                for e in data.get('E', [])
            )

        for ssn_raw, serial_list in self.patient_ssn_index.items():

            # ── 그룹 A: EB511/EB512 ────────────────────────────────────────
            early_serials = []
            for sno in serial_list:
                data = self.patients_db.get(sno, {})
                has_early = any(
                    any(code in c.get('treat_code', '').upper() for code in EARLY_US_CODES)
                    for c in data.get('C', [])
                )
                if has_early:
                    early_serials.append((get_date_str(data), sno))

            if len(early_serials) > 2:
                early_serials.sort(key=lambda x: x[0])
                total_us_a     = len(early_serials)
                required_a     = total_us_a - 2  # 첫 2회 면제

                # 그룹 전체 JX999 합산 (어느 명세서에 있든 상관없음)
                total_jx999_a = sum(
                    1 for _, sno in early_serials
                    for e in self.patients_db[sno].get('E', [])
                    if e.get('spec_code', '').strip().upper() == 'JX999'
                )

                if total_jx999_a < required_a:
                    shortage_a = required_a - total_jx999_a
                    # JX999 없는 명세서(3번째 이후) 중 부족분만큼 에러 표시
                    no_memo_a = [
                        (d, s) for d, s in early_serials[2:]
                        if not check_jx999(self.patients_db[s])
                    ]
                    for date_str, sno in no_memo_a[:shortage_a]:
                        data = self.patients_db[sno]
                        data['AUDIT'].append((
                            sno,
                            "청구메모 누락(초음파통합)",
                            f"EB511/512 ({total_us_a}회/{shortage_a}건 부족)",
                            f"동일 환자 EB511/EB512 {total_us_a}회 → "
                            f"JX999 {required_a}건 필요 / {total_jx999_a}건 있음 "
                            f"({shortage_a}건 부족) — 내원일 {date_str} 명세서 확인 필요"
                        ))
                        problematic_pids.add(sno)
                        total_errors += 1

            # ── 그룹 B: 1회 기본 그룹 (일반/정밀 별개 독립 카운팅) ──────────
            # 일반과 정밀은 서로 다른 급여 항목이므로 절대 합산하지 않음
            # 각 그룹 전체 JX999 총 개수로 판정 (어느 명세서에 있든 무관)
            single_free_groups = [
                ("1삼분기 정밀",    FIRST_TRI_DETAIL_CODES),
                ("2,3삼분기 일반",  SECOND_THIRD_GENERAL_CODES),
                ("2,3삼분기 정밀",  SECOND_THIRD_DETAIL_CODES),
            ]

            for group_name, group_codes in single_free_groups:
                group_serials = []
                for sno in serial_list:
                    data = self.patients_db.get(sno, {})
                    has_code = any(
                        any(code in c.get('treat_code', '').upper() for code in group_codes)
                        for c in data.get('C', [])
                    )
                    if has_code:
                        group_serials.append((get_date_str(data), sno))

                if len(group_serials) <= 1:
                    continue  # 1회 이하는 심사 불필요

                group_serials.sort(key=lambda x: x[0])
                total_us     = len(group_serials)
                required     = total_us - 1  # 첫 1회 면제

                # 그룹 전체 JX999 합산
                total_jx999 = sum(
                    1 for _, sno in group_serials
                    for e in self.patients_db[sno].get('E', [])
                    if e.get('spec_code', '').strip().upper() == 'JX999'
                )

                if total_jx999 >= required:
                    continue  # 전체 메모 수 충족 → 통과

                # 부족한 경우: JX999 없는 명세서(2번째 이후) 중 부족분만큼 에러
                shortage = required - total_jx999
                no_memo = [
                    (d, s) for d, s in group_serials[1:]
                    if not check_jx999(self.patients_db[s])
                ]
                for date_str, sno in no_memo[:shortage]:
                    data = self.patients_db[sno]
                    data['AUDIT'].append((
                        sno,
                        "청구메모 누락(초음파통합)",
                        f"{group_name} ({total_us}회/{shortage}건 부족)",
                        f"동일 환자 {group_name} {total_us}회 → "
                        f"JX999 {required}건 필요 / {total_jx999}건 있음 "
                        f"({shortage}건 부족) — 내원일 {date_str} 명세서 확인 필요"
                    ))
                    problematic_pids.add(sno)
                    total_errors += 1

        # 심사 완료 후 목록 갱신
        self.refresh_patient_list(self.search_var.get())
        sel = self.tree_patients.selection()
        if sel:
            self.on_patient_select(None)

        messagebox.showinfo(
            "심사 완료",
            f"전체 환자 사전심사가 완료되었습니다.\n"
            f"발견된 총 위험 건수: {total_errors}건\n\n"
            f"💡 팁: '확인필요' 글자를 클릭하시면 문제 환자만 모아서 볼 수 있습니다."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = SinglePageReviewApp(root)
    root.mainloop()