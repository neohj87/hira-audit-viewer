import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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
# UI 디스플레이 컬럼 (화면에 보여줄 필수 컬럼)
# ==============================================================================
DISPLAY_COLUMNS = {
    'A': ["serial_no", "medical_care_type", "first_admit_date", "patient_name", "patient_ssn", "care_days", "patient_amt","total_amt_1", "claim_amt"],
    'B': ["sick_type_div", "sick_code", "treat_dept", "treat_start_date", "doc_license_no"],
    'C': ["category", "line_no", "code_div", "treat_code", "unit_price", "day_dose", "total_days", "amount"],
    'D': ["presc_issue_no", "line_no", "code_div", "medi_code", "dose_per_once", "total_presc_days"],
    'E': ["line_no", "spec_code", "spec_detail"]
}

# ==============================================================================
# 2. 메인 어플리케이션
# ==============================================================================
class SinglePageReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("심평원 청구데이터 사전심사 시스템 v2.8 (스크롤 & 건수 UI 추가)")
        self.root.geometry("1450x950")
        
        self.h_record = {}
        self.patients_db = {}
        self.audit_run = False 
        
        self._build_ui()

    def _build_ui(self):
        # 상단 패널
        top_frame = tk.Frame(self.root, bg="#2C5282", pady=10, padx=10)
        top_frame.pack(fill=tk.X)
        tk.Label(top_frame, text="🏥 HIRA 통합 사전심사 뷰어", fg="white", bg="#2C5282", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        btn_audit = tk.Button(top_frame, text="🚨 사전심사 실행", font=("Arial", 10, "bold"), bg="#E53E3E", fg="white", command=self.run_audit)
        btn_audit.pack(side=tk.RIGHT, padx=5)
        
        btn_load = tk.Button(top_frame, text="📂 EDI 청구파일(.B02) 불러오기", font=("Arial", 10, "bold"), command=self.load_file)
        btn_load.pack(side=tk.RIGHT, padx=5)

        # 메인 패널 분할
        main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # -------------------------------------------------------------
        # [좌측] 환자 목록 영역 (스크롤바 & 건수 표시 추가)
        # -------------------------------------------------------------
        left_frame = ttk.LabelFrame(main_pane, text=" 수진자 목록 ")
        main_pane.add(left_frame, weight=1)
        
        # 검색 프레임
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=15)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        search_entry.insert(0, "코드 검색...")
        
        def on_entry_click(event):
            if self.search_var.get() == "코드 검색...": search_entry.delete(0, "end")
        def on_focusout(event):
            if self.search_var.get() == "": search_entry.insert(0, "코드 검색...")
            
        search_entry.bind('<FocusIn>', on_entry_click)
        search_entry.bind('<FocusOut>', on_focusout)
        search_entry.bind("<Return>", lambda e: self.search_patients())
        
        btn_search = ttk.Button(search_frame, text="검색", command=self.search_patients, width=4)
        btn_search.pack(side=tk.LEFT, padx=1)
        btn_reset = ttk.Button(search_frame, text="초기화", command=self.reset_search, width=5)
        btn_reset.pack(side=tk.LEFT)

        # 💡 트리뷰와 스크롤바를 묶어줄 컨테이너 프레임
        tree_container = ttk.Frame(left_frame)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=0)

        style = ttk.Style()
        style.map("Treeview", foreground=self.fixed_map("foreground"), background=self.fixed_map("background"))
        
        self.tree_patients = ttk.Treeview(tree_container, columns=("id", "name", "status"), show="headings")
        self.tree_patients.heading("id", text="명일련", command=lambda c="id": self.sort_tree(self.tree_patients, c, False))
        self.tree_patients.heading("name", text="수진자명", command=lambda c="name": self.sort_tree(self.tree_patients, c, False))
        self.tree_patients.heading("status", text="확인필요", command=lambda c="status": self.sort_tree(self.tree_patients, c, True))
        
        self.tree_patients.column("id", width=50, anchor="center")
        self.tree_patients.column("name", width=70, anchor="center")
        self.tree_patients.column("status", width=60, anchor="center")
        self.tree_patients.bind("<<TreeviewSelect>>", self.on_patient_select)

        # 💡 환자 목록용 세로 스크롤바 장착
        vsb_patients = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree_patients.yview)
        self.tree_patients.configure(yscrollcommand=vsb_patients.set)
        
        self.tree_patients.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb_patients.pack(side=tk.RIGHT, fill=tk.Y)

        # 💡 건수 표시 상태 표시줄(Label) 추가
        self.lbl_patient_count = tk.Label(left_frame, text="전체: 0명 / 조회: 0명", fg="#2C5282", font=("Arial", 10, "bold"), bg="#e2e8f0", pady=3)
        self.lbl_patient_count.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)


        # -------------------------------------------------------------
        # [우측] 통합 스크롤 영역
        # -------------------------------------------------------------
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=5)
        
        canvas = tk.Canvas(right_frame)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        right_frame.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.trees = {}
        sections = [
            ("A", "명세서 일반내역 (A)", 1), 
            ("B", "상병내역 (B)", 3),
            ("C", "진료내역 (C)", 6),
            ("D", "처방내역 (D)", 3),
            ("E", "특정내역기재란 (E)", 3),
            ("AUDIT", "🚨 사전심사 결과 (선택된 환자 기준)", 4)
        ]
        
        for key, title, h_lines in sections:
            lf = ttk.LabelFrame(self.scrollable_frame, text=f" {title} ")
            lf.pack(fill=tk.X, expand=True, padx=5, pady=10)
            
            if key == "AUDIT":
                cols = ("id", "type", "code", "msg")
                tree = ttk.Treeview(lf, columns=cols, show="headings", height=h_lines)
                tree.heading("id", text="명일련")
                tree.heading("type", text="심사유형")
                tree.heading("code", text="관련코드")
                tree.heading("msg", text="심사/조정 메시지")
                tree.column("id", width=60, anchor="center")
                tree.column("type", width=100, anchor="center")
                tree.column("code", width=100, anchor="center")
                tree.column("msg", width=500, anchor="w")
            else:
                schema = SCHEMAS[key]
                display_cols = DISPLAY_COLUMNS[key]
                tree = ttk.Treeview(lf, columns=display_cols, show="headings", height=h_lines)
                
                for c in display_cols:
                    kor_name = schema[c][3]
                    tree.heading(c, text=kor_name)
                    w = 400 if c == "spec_detail" else 100
                    tree.column(c, width=w, anchor="center" if "name" not in c and "detail" not in c else "w")
            
            vsb = ttk.Scrollbar(lf, orient="vertical", command=tree.yview)
            hsb = ttk.Scrollbar(lf, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            tree.grid(row=0, column=0, sticky='nsew')
            vsb.grid(row=0, column=1, sticky='ns')
            hsb.grid(row=1, column=0, sticky='ew')
            
            lf.grid_columnconfigure(0, weight=1)
            lf.grid_rowconfigure(0, weight=1)
            
            self.trees[key] = tree

    def fixed_map(self, option):
        return [elm for elm in ttk.Style().map("Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]

    def sort_tree(self, tree, col, reverse):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)
        tree.heading(col, command=lambda: self.sort_tree(tree, col, not reverse))

    # ==============================================================================
    # 환자 목록 갱신 및 필터링(검색) + 건수 표시 기능
    # ==============================================================================
    def refresh_patient_list(self, search_keyword=""):
        for item in self.tree_patients.get_children():
            self.tree_patients.delete(item)
            
        search_keyword = search_keyword.strip().upper()
        if search_keyword == "코드 검색...":
            search_keyword = ""

        total_patients = len(self.patients_db)
        filtered_count = 0

        for p_id, data in self.patients_db.items():
            if search_keyword:
                found = False
                if any(search_keyword in b.get('sick_code', '').upper() for b in data['B']):
                    found = True
                elif any(search_keyword in c.get('treat_code', '').upper() for c in data['C']):
                    found = True
                
                if not found:
                    continue
            
            status_mark = "❗" if len(data.get('AUDIT', [])) > 0 else ""
            self.tree_patients.insert("", "end", values=(p_id, data["name"], status_mark))
            filtered_count += 1

        # 💡 상태 라벨 텍스트 즉시 업데이트!
        self.lbl_patient_count.config(text=f"전체: {total_patients}명 / 조회: {filtered_count}명")

    def search_patients(self):
        if not self.patients_db: return
        keyword = self.search_var.get()
        self.refresh_patient_list(keyword)

    def reset_search(self):
        if not self.patients_db: return
        self.search_var.set("코드 검색...")
        self.refresh_patient_list("") 

    # ==============================================================================
    # 3. 무결점 바이트 파싱 엔진 (계산 로직 제거 버전)
    # ==============================================================================
    def parse_bytes_line(self, b_line, schema, rec_type):
        parsed_data = {}
        max_len = max([pos + length - 1 for pos, length, _, _ in schema.values()])
        if len(b_line) < max_len:
            b_line = b_line.ljust(max_len, b' ')

        for var_name, (pos, length, dec, kor_name) in schema.items():
            chunk = b_line[pos-1 : pos-1+length]
            val_str = chunk.decode('cp949', errors='ignore').strip()
            
            is_number = dec >= 0 and any(kw in kor_name for kw in ["금액", "일수", "횟수", "건수", "의사수", "량", "단가", "지수", "총액", "의료비", "대불금"])
            is_except = any(kw in kor_name for kw in ["번호", "기호", "코드", "구분", "ID", "일련", "성명", "기관", "경로", "결과"])
            
            if is_number and not is_except:
                try:
                    num = float(val_str) if val_str else 0.0
                    
                    if rec_type == 'C':
                        if var_name == "unit_price":      
                            num = num / 10000
                        elif var_name == "amount":         
                            num = num / 100
                        elif var_name == "day_dose":
                            num = num / 10000
                        elif var_name == "total_days": 
                            num = num / 100
                    
                    elif rec_type == 'D':
                        # D그룹의 '1회투약량(dose_per_once)'을 10,000으로 나눔
                        if var_name == "dose_per_once":
                            num = num / 10000
                    
                    # 출력 처리
                    if num.is_integer():
                        parsed_data[var_name] = f"{int(num):,}"
                    else:
                        parsed_data[var_name] = f"{num:,.{dec}f}"
                except ValueError:
                    parsed_data[var_name] = "0"
            else:
                if var_name == "patient_ssn" and len(val_str) == 13:
                    parsed_data[var_name] = val_str[:6] + "-*******"
                else:
                    parsed_data[var_name] = val_str
                    
        return parsed_data
    # ==============================================================================
    # 파일 로드
    # ==============================================================================
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("EDI Files", "*.B02")])
        if not file_path: return
        
        self.h_record = {}
        self.patients_db = {}
        self.audit_run = False 
        
        with open(file_path, 'rb') as f:
            for raw_line in f:
                b_line = raw_line.replace(b'\xef\xbb\xbf', b'').replace(b'\r', b'').replace(b'\n', b'')
                if len(b_line) < 15: continue
                
                if b_line.startswith(b"090") or b_line.startswith(b"092"):
                    rec_type = 'H'
                else:
                    rec_type = b_line[15:16].decode('cp949', errors='ignore')
                
                if rec_type not in SCHEMAS: continue
                
                # 💡 여기가 수정되었습니다! rec_type을 인자로 전달합니다.
                parsed = self.parse_bytes_line(b_line, SCHEMAS[rec_type], rec_type)
                
                if rec_type == 'H':
                    self.h_record = parsed 
                else:
                    p_id = parsed.get("serial_no", "")
                    if not p_id: continue
                    
                    if p_id not in self.patients_db:
                        self.patients_db[p_id] = {"name": "", "A": [], "B": [], "C": [], "D": [], "E": [], "AUDIT": []}
                    
                    if rec_type == 'A':
                        name_val = parsed.get("patient_name", "").strip()
                        self.patients_db[p_id]["name"] = name_val if name_val else "이름없음"
                    
                    self.patients_db[p_id][rec_type].append(parsed)

        self.search_var.set("코드 검색...")
        self.refresh_patient_list("")

        for t in ['A', 'B', 'C', 'D', 'E', 'AUDIT']:
            for item in self.trees[t].get_children(): self.trees[t].delete(item)

        messagebox.showinfo("로드 완료", f"파일 파싱 성공! (총 환자: {len(self.patients_db)}명)")
    # ==============================================================================
    # 환자 선택 이벤트
    # ==============================================================================
    def on_patient_select(self, event):
        sel = self.tree_patients.selection()
        if not sel: return
        p_id = self.tree_patients.item(sel[0], "values")[0]
        data = self.patients_db[p_id]

        for t in ['A', 'B', 'C', 'D', 'E']:
            tree = self.trees[t]
            for item in tree.get_children(): tree.delete(item)
            
            for row_dict in data[t]:
                vals = [row_dict.get(c, "") for c in DISPLAY_COLUMNS[t]]
                tree.insert("", "end", values=vals)

        tree_audit = self.trees['AUDIT']
        for item in tree_audit.get_children(): tree_audit.delete(item)
        
        if not self.audit_run:
            tree_audit.insert("", "end", values=(p_id, "안내", "-", "상단의 [사전심사 실행] 버튼을 눌러주세요."))
        elif not data['AUDIT']:
            tree_audit.insert("", "end", values=(p_id, "심사통과", "-", "발견된 삭감/조정 위험이 없습니다. 청구 가능!"))
        else:
            for res in data['AUDIT']:
                tree_audit.insert("", "end", values=res)

    # ==============================================================================
    # 6. 사전심사 로직 (EB516 조건 추가)
    # ==============================================================================
    def run_audit(self):
        if not self.patients_db:
            messagebox.showwarning("경고", "먼저 청구 파일을 불러와주세요.")
            return
            
        self.audit_run = True 
        problematic_pids = set()
        total_errors = 0
        
        for p_id, data in self.patients_db.items():
            data['AUDIT'] = [] 
            
            if not data.get('C'):
                continue
            
            # -------------------------------------------------------------
            # [심사조건 1] 초음파(EB455) JX999 누락 검사
            # -------------------------------------------------------------
            has_eb455 = any("EB455" in c_row.get('treat_code', '').upper() for c_row in data['C'])
            if has_eb455:
                if not data.get('E'):
                    has_jx999 = False
                else:
                    has_jx999 = any(e_row.get('spec_code', '').strip().upper() == 'JX999' for e_row in data['E'])
                
                if not has_jx999:
                    data['AUDIT'].append((p_id, "청구메모 미기재", "EB455", "진단초음파(EB455)가 청구되었으나, 특정내역(JX999) 메모가 누락되었습니다."))
                    problematic_pids.add(p_id)
                    total_errors += 1

            # -------------------------------------------------------------
            # [심사조건 6] 수가코드 ID602 처방 시 특정내역(JT041) 필수
            # -------------------------------------------------------------
            has_602 = any("ID602" in c_row.get('treat_code', '').upper() for c_row in data.get('C', []))
            
            if has_602:
                # 특정내역(E)에서 JT041가 있는지 확인
                has_jt041 = any(e_row.get('spec_code', '').strip().upper() == 'JT041' for e_row in data.get('E', []))
                
                if not has_jt041:
                    data['AUDIT'].append((
                        p_id, 
                        "청구메모 미기재", 
                        "ID602", 
                        "수가코드 ID602 청구 시 특정내역(JT041) 기재가 필수이나 누락되었습니다."
                    ))
                    problematic_pids.add(p_id)
                    total_errors += 1

            # -------------------------------------------------------------
            # [심사조건 2] R4106 수가 검사 (B373 또는 N72 필수)
            # -------------------------------------------------------------
            has_r4106 = any("R4106" in c_row.get('treat_code', '').upper() for c_row in data['C'])
            if has_r4106:
                if not data.get('B'):
                    has_required_sick = False
                else:
                    has_required_sick = any(
                        "B373" in b_row.get('sick_code', '').upper() or 
                        "N72" in b_row.get('sick_code', '').upper() 
                        for b_row in data['B']
                    )
                
                if not has_required_sick:
                    data['AUDIT'].append((p_id, "상병누락", "R4106", "R4106 수가 청구 시 B373 또는 N72 상병코드 중 최소 하나가 필요합니다."))
                    problematic_pids.add(p_id)
                    total_errors += 1

            # -------------------------------------------------------------
            # 💡 [심사조건 3] 초음파(EB516) JX999 누락 검사 (신규 추가!)
            # -------------------------------------------------------------
            has_eb516 = any("EB516" in c_row.get('treat_code', '').upper() for c_row in data['C'])
            if has_eb516:
                if not data.get('E'):
                    has_jx999 = False
                else:
                    has_jx999 = any(e_row.get('spec_code', '').strip().upper() == 'JX999' for e_row in data['E'])
                
                if not has_jx999:
                    data['AUDIT'].append((p_id, "청구메모 미기재", "EB516", "고위험 초음파(EB516)가 청구되었으나, 특정내역(JX999) 메모가 누락되었습니다."))
                    problematic_pids.add(p_id)
                    total_errors += 1
          # -------------------------------------------------------------
            # [수정된 심사조건 4] 다태아(O300) 산전 검사 청구 누락 체크
            # -------------------------------------------------------------
            # A영역이 아니라 B영역의 sick_code를 확인해야 합니다.
            is_twin = any("O300" in b_row.get('sick_code', '').upper() for b_row in data.get('B', []))
            
            if is_twin:
                twin_target_codes = [
                    "EB511", "EB512", "EB513", "EB514", "EB515", "EB517", "EB518", 
                    "E7326"
                ]
                
                for c_row in data['C']:
                    code = c_row.get('treat_code', '').upper()
                    if any(target in code for target in twin_target_codes):
                        try:
                            dose = float(c_row.get('day_dose', 0))
                            if dose < 1.5:
                                data['AUDIT'].append((
                                    p_id, 
                                    "청구 누락(다태아)", 
                                    code, 
                                    f"다태아(O300) 환자입니다. {code}는 1.5배 청구 가능하나 현재 {dose}로 청구되었습니다."
                                ))
                                problematic_pids.add(p_id)
                                total_errors += 1
                        except ValueError:
                            continue
            # -------------------------------------------------------------
            # [심사조건 5] 약제별 필수 상병 매핑 체크
            # -------------------------------------------------------------
            # {약제코드: [필수상병코드들]} 형태로 규칙을 정의합니다.
            REQUIRED_RULES = {
                "652601250": ["B373"],
                "671800840": ["B373"]
            }
            
            for d_row in data.get('D', []):
                medi_code = d_row.get('medi_code', '').strip()
                
                # 처방된 약제가 규칙에 포함되어 있다면?
                if medi_code in REQUIRED_RULES:
                    required_sicks = REQUIRED_RULES[medi_code]
                    
                    # 해당 환자의 상병 내역(B)에 필수 상병이 하나라도 있는지 확인
                    has_required = any(
                        s in b_row.get('sick_code', '').upper() 
                        for b_row in data.get('B', []) 
                        for s in required_sicks
                    )
                    
                    if not has_required:
                        data['AUDIT'].append((
                            p_id, 
                            "상병누락(약제)", 
                            medi_code, 
                            f"약제({medi_code}) 처방 시 {required_sicks} 상병이 필수이나 누락되었습니다."
                        ))
                        problematic_pids.add(p_id)
                        total_errors += 1
            
            from datetime import datetime

            # -------------------------------------------------------------
            # [심사조건 7] 비자극검사(E7325) 2회차 심사 (나이 & 메모)
            # -------------------------------------------------------------
            # 1. 먼저 E7325가 2회 이상인지 확인
            e7325_list = [c_row for c_row in data.get('C', []) if "E7325" in c_row.get('treat_code', '').upper()]
            
            if len(e7325_list) >= 2:
                # 2. 주민번호 추출
                ssn = next((a_row.get('patient_ssn', '') for a_row in data.get('A', [])), "")
                
                # 주민번호가 7자리 이상(성별코드 포함)이어야 나이 계산 가능
                if len(ssn) >= 7:
                    gender_code = ssn[6]
                    if gender_code in ['1', '2', '5', '6']:
                        birth_year_prefix = "19"
                    elif gender_code in ['3', '4', '7', '8']:
                        birth_year_prefix = "20"
                    else:
                        birth_year_prefix = "19" # 기본값
                        
                    birth_date_str = birth_year_prefix + ssn[:6]
                    
                    try:
                        birth_date = datetime.strptime(birth_date_str, "%Y%m%d")
                        today = datetime.now()
                        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                        
                        # 만 35세 심사 로직
                        if age <= 35:
                            data['AUDIT'].append((
                                p_id, "삭감주의(나이제한)", "E7325", f"만 {age}세로 2회차 청구 시 삭감 대상입니다."
                            ))
                            problematic_pids.add(p_id)
                            total_errors += 1
                        else:
                            # 35세 초과 시 JX999 메모 체크
                            has_jx999 = any(e_row.get('spec_code', '').strip().upper() == 'JX999' for e_row in data.get('E', []))
                            if not has_jx999:
                                data['AUDIT'].append((
                                    p_id, "청구 누락(횟수초과)", "E7325", "만 35세 초과자 2회차 청구 시 특정내역(JX999)이 필수이나 누락되었습니다."
                                ))
                                problematic_pids.add(p_id)
                                total_errors += 1
                    except ValueError:
                        pass # 날짜 형식이 이상할 경우 패스
            

        # 심사가 끝나면, '현재 입력되어 있는 검색어'를 유지한 채로 리스트를 새로고침하여 ❗ 마크를 입힘
        current_keyword = self.search_var.get()
        self.refresh_patient_list(current_keyword)

        sel = self.tree_patients.selection()
        if sel:
            self.on_patient_select(None)
            
        messagebox.showinfo("심사 완료", f"전체 환자 사전심사가 완료되었습니다.\n발견된 총 위험 건수: {total_errors}건\n\n💡 팁: '확인필요' 글자를 클릭하시면 문제 환자만 모아서 볼 수 있습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SinglePageReviewApp(root)
    root.mainloop()