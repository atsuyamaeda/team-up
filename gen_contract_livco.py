#!/usr/bin/env python3
"""
業務委託個別契約書 PDF生成スクリプト — 株式会社リブコ向け
クラウドサイン登録用（A4縦）
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, black

# ── フォント登録 ──────────────────────────────────────────────
FONT_REGULAR = '/Users/maedaatsuya/Downloads/NotoSerifJP-Regular.ttf'
FONT_LIGHT   = '/Users/maedaatsuya/Downloads/NotoSerifJP-Light.ttf'
pdfmetrics.registerFont(TTFont('NotoSerif',   FONT_REGULAR))
pdfmetrics.registerFont(TTFont('NotoSerif-L', FONT_LIGHT))

# ── 出力先 ────────────────────────────────────────────────────
OUT = '/Users/maedaatsuya/team-up/contract_livco.pdf'

# ── カラー ────────────────────────────────────────────────────
DARK  = HexColor('#111111')
GRAY  = HexColor('#555555')
LGRAY = HexColor('#aaaaaa')
RULE  = HexColor('#dddddd')

# ── スタイル定義 ──────────────────────────────────────────────
def S(name, **kw):
    """ParagraphStyleのショートハンド（デフォルト：NotoSerif-L, DARK, leading=18）"""
    defaults = dict(fontName='NotoSerif-L', textColor=DARK, leading=18)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)


def make_styles():
    return {
        'title':        S('title',
                          fontName='NotoSerif', fontSize=16,
                          alignment=TA_CENTER, spaceAfter=6*mm, leading=24),
        'preamble':     S('preamble',
                          fontSize=9, alignment=TA_JUSTIFY, spaceAfter=4*mm),
        'article_head': S('article_head',
                          fontName='NotoSerif', fontSize=10,
                          spaceBefore=6*mm, spaceAfter=2*mm, leading=16),
        'body':         S('body',
                          fontSize=9, alignment=TA_JUSTIFY,
                          spaceAfter=1.5*mm, leftIndent=4*mm),
        'body_indent':  S('body_indent',
                          fontSize=9, alignment=TA_JUSTIFY,
                          spaceAfter=1.5*mm, leftIndent=10*mm),
        'note':         S('note',
                          fontSize=8, textColor=GRAY, alignment=TA_JUSTIFY,
                          spaceAfter=1.5*mm, leftIndent=4*mm, leading=14),
        'sig_label':    S('sig_label',
                          fontSize=9, textColor=GRAY, spaceAfter=1*mm),
        'sig_value':    S('sig_value',
                          fontName='NotoSerif', fontSize=9, spaceAfter=2*mm, leading=16),
        'footer_note':  S('footer_note',
                          fontSize=8, textColor=LGRAY,
                          alignment=TA_CENTER, spaceBefore=4*mm),
    }


def build():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=25*mm, rightMargin=25*mm,
        topMargin=20*mm,  bottomMargin=20*mm,
        title='業務委託個別契約書',
        author='株式会社Duality',
    )

    S = make_styles()
    story = []

    # ────── タイトル ──────────────────────────────────────────
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('業務委託個別契約書', S['title']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=RULE, spaceAfter=4*mm))

    # ────── 前文 ──────────────────────────────────────────────
    story.append(Paragraph(
        '＿＿＿＿＿＿＿＿＿＿（以下「甲」という）と株式会社Duality（以下「乙」という）は、'
        '業務委託個別契約（以下「本契約」という）を次のとおり締結する。',
        S['preamble']
    ))

    # ────── 条文データ ────────────────────────────────────────
    articles = [

        ('第１条（業務内容）', [
            ('body', '１．甲は乙に対し、以下の業務（以下「本業務」という）を委託し、乙はこれを受託する。'),
            ('body_indent', '（１）採用戦略の立案・企画'),
            ('body_indent', '（２）母集団形成に関する施策の企画および提案'),
            ('body_indent', '（３）採用媒体選定およびスカウト活用方針の策定'),
            ('body_indent', '（４）採用KPIの策定およびレポーティング（定例報告含む）'),
            ('body_indent', '（５）その他付随する業務'),
            ('body', '２　甲は本件業務の遂行に際し必要があるときは、乙に対し、本件業務の進捗状況などについて報告を求めることができる。'),
        ]),

        ('第２条（成果物）', [
            ('body', '乙は甲に、下記の成果物を納入する。'),
            ('body_indent', '（１）都度指定'),
        ]),

        ('第３条（提携料）', [
            ('body', '１　甲は乙に対し、月額金６００，０００円（税抜）を支払うこととする。'),
            ('body_indent', '月間稼働時間：６０時間'),
            ('note',
             '※月間稼働時間が６０時間に満たない場合、もしくは超過して稼働した場合には、'
             '乙が現実に行った本件業務の時間数に応じて、１時間あたり金１０，０００円（税抜）として'
             '算出した差額を加減して精算するものとする。'
             'なお、６０時間を超過して稼働する場合には、事前に甲の書面による承認を得るものとする。'),
            ('body', '２　甲は、前項に定める提携料の当月分を翌月末日に、乙の指定する銀行口座に振り込む方法によって支払う。なお、振込手数料は甲の負担とする。消費税及び地方消費税は別途甲の負担とする。'),
        ]),

        ('第４条（契約期間・契約更新）', [
            ('body', '１　契約期間は、２０２６年３月９日〜２０２６年６月８日（３ヶ月間）とする。'),
            ('body', '２　委託期間終了日の１ヶ月前までに、甲乙いずれからも何ら申し出のないときは、本契約と同一の条件で自動更新するものとし、以後同様とする。（１ヶ月更新）'),
            ('body', '３　本契約終了後も第６条乃至第９条、第１４条、第１５条及び本項の規定は有効に存続するものとする。'),
        ]),

        ('第５条（稼働時間の記録・報告）', [
            ('body', '１　乙は、甲が指定するツールおよび方法により、日々の稼働時間を記録するものとする。'),
            ('body', '２　乙は、毎月末日までに当月分の稼働時間を甲に報告するものとする。'),
            ('body', '３　甲は、報告された稼働時間を確認し、疑義がある場合は乙に確認を求めることができる。'),
        ]),

        ('第６条（秘密保持）', [
            ('body', '１　甲と乙は、本業務に関して知り得た相手方の技術、財務、営業、販売、その他の業務に関する秘密情報を、相手方の事前の書面による承諾なしに第三者に漏洩してはならない。'),
            ('body', '２　前項の秘密保持義務は、本契約終了後２年間存続するものとする。'),
            ('body', '３　以下のいずれかに該当する情報は秘密情報に含まないものとする。'),
            ('body_indent', '（１）開示時点で既に公知であった情報'),
            ('body_indent', '（２）開示後に受領者の責によらず公知となった情報'),
            ('body_indent', '（３）受領者が開示を受ける前から正当に保有していた情報'),
            ('body_indent', '（４）受領者が独自に開発した情報'),
            ('body_indent', '（５）法令または裁判所・行政機関の命令に基づき開示が求められた情報（必要最小限の範囲に限る）'),
        ]),

        ('第７条（著作権の帰属）', [
            ('body', '本件業務に係わる著作権は、甲に帰属するものとする。ただし、乙が従前から有していた既存の著作権'
             '（ノウハウ、フレームワーク、テンプレート等を含む）を利用しているものについては、乙に帰属するものとし、'
             '乙は甲に対し本業務の遂行目的に限り無償で利用を許諾するものとする。'),
        ]),

        ('第８条（第三者の権利侵害）', [
            ('body', '乙は、本件業務の遂行過程において甲に提供する業務関連資料が第三者の著作権、肖像権、特許権および'
             'その他一切の権利を侵害していないことを保証する。'),
        ]),

        ('第９条（損害賠償）', [
            ('body', '１　甲および乙は、本契約に関連して相手方の責めに帰すべき事由により損害を被った場合には、相手方に対しその賠償を請求することができる。'),
            ('body', '２　乙の損害賠償責任は、故意または重過失による場合を除き、損害発生の原因となった業務が遂行された月の提携料相当額を上限とする。'),
        ]),

        ('第１０条（権利義務の譲渡及び再委託の禁止）', [
            ('body', '１　甲及び乙は、相手方の事前の書面による承諾なく本契約に基づく権利あるいは義務を第三者に譲渡し、引受けさせ、又は担保に供してはならない。'),
            ('body', '２　乙は、委託業務を第三者に委託してはならない。但し、甲の事前の書面による承諾がある場合、本契約において自らが負うと同様の義務を課することを条件として、委託業務の全部あるいは一部を当該第三者に委託することができるものとし、当該第三者の行為について連帯して責任を負うものとする。'),
        ]),

        ('第１１条（解約・中途解除）', [
            ('body', '１　甲または乙が契約期間中に本契約を解約しようとするときは、解約希望日の１ヶ月前までに相手方に対して書面により通知しなければならない。'),
            ('body', '２　前項にかかわらず、甲または乙が次の各号のいずれかに該当したときは、その相手方は催告その他の手続を要することなく、直ちに本契約を解除することができる。'),
            ('body_indent', '（１）破産、特別清算、民事再生手続もしくは会社更生手続開始の申立を受け、または自らこれらの一を申し立てたとき'),
            ('body_indent', '（２）第三者より差押、仮差押、仮処分、強制執行もしくは競売申立てまたは公租公課滞納処分を受けたとき'),
            ('body_indent', '（３）監督官庁より営業の取消、停止等の処分を受けたとき'),
            ('body_indent', '（４）解散、減資、営業の全部または重要な一部の譲渡等の決議をしたとき'),
            ('body_indent', '（５）自ら振出し、または引き受けた手形、小切手が不渡り処分になる等、支払いが不能な状態になったとき'),
            ('body_indent', '（６）相手方が本契約の各条項に重大な違反をし、相当期間（７日間以上）を定めた催告の後もなお是正されないとき'),
            ('body_indent', '（７）相手方に重大な過失または背信行為があったとき'),
            ('body_indent', '（８）その他本契約を継続しがたい重大な事由が発生したとき'),
            ('body', '３　理由の如何を問わず本契約が終了した場合、甲は終了日までに乙が遂行した業務に対する報酬を精算の上支払うものとする。'),
        ]),

        ('第１２条（不可抗力）', [
            ('body', '天災地変、感染症の蔓延、戦争、法令の改廃、通信障害その他の不可抗力により、本契約に基づく義務の全部または一部の履行が困難となった場合、いずれの当事者も相手方に対して責任を負わないものとする。ただし、不可抗力の影響を受けた当事者は、速やかに相手方に通知するものとする。'),
        ]),

        ('第１３条（反社会的勢力の排除）', [
            ('body', '１　甲及び乙は、相手方に対し、本契約締結時及び本契約締結後において、自己が暴力団、暴力団関係企業・団体その他反社会的勢力（以下「反社会的勢力」という。）ではないこと、反社会的勢力の支配・影響を受けていないこと、及び自己の役員、従業員、関係者等が反社会的勢力の構成員またはその関係者ではないことを表明し、保証する。'),
            ('body', '２　甲又は乙は、相手方が前項の表明・保証に違反した場合、通知・催告その他の手続きを要せずに本件に関する一切の取引を解除することができる。'),
        ]),

        ('第１４条（裁判管轄）', [
            ('body', '本契約に関する一切の争訟は、東京地方裁判所を第一審の専属管轄裁判所とする。'),
        ]),

        ('第１５条（協議）', [
            ('body', '本契約に定めのない事項、または本契約の解釈等に疑義が生じたときは、甲乙は誠意を持って協議し、円満に解決を図るものとする。'),
        ]),
    ]

    # ────── 各条文を描画 ─────────────────────────────────────
    for (heading, paragraphs) in articles:
        block = [Paragraph(heading, S['article_head'])]
        for style_key, text in paragraphs:
            block.append(Paragraph(text, S[style_key]))
        story.append(KeepTogether(block))

    # ────── 締結文・署名欄 ────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width='100%', thickness=0.5, color=RULE, spaceAfter=4*mm))
    story.append(Paragraph(
        '本契約は、電子契約サービス「クラウドサイン」を利用して締結するものとし、'
        'クラウドサインにより締結された電子文書をもって原本とする。',
        S['preamble']
    ))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('　　　　年　　月　　日', S['body']))
    story.append(Spacer(1, 6*mm))

    # 署名テーブル（2列）
    sig_data = [
        [
            # 甲 欄
            Table([
                [Paragraph('甲', S['article_head'])],
                [Paragraph('住所　　　　　　　　　　　　　　　　　　　　　　', S['sig_label'])],
                [Paragraph('　　　　　　　　　　　　　　　　　　　　　　　　', S['sig_label'])],
                [Paragraph('商号　　　　　　　　　　　　　　　　　　　　　　', S['sig_label'])],
                [Paragraph('代表取締役　　　　　　　　　　　㊞', S['sig_label'])],
            ], colWidths=[75*mm],
               style=TableStyle([
                   ('LINEBELOW', (0,1),(0,1), 0.5, RULE),
                   ('LINEBELOW', (0,2),(0,2), 0.5, RULE),
                   ('LINEBELOW', (0,3),(0,3), 0.5, RULE),
                   ('LINEBELOW', (0,4),(0,4), 0.5, RULE),
               ])),
            # 乙 欄
            Table([
                [Paragraph('乙', S['article_head'])],
                [Paragraph('住所　東京都新宿区新宿2-2-1', S['sig_label'])],
                [Paragraph('　　　ビューシティ新宿御苑1402', S['sig_label'])],
                [Paragraph('株式会社Duality', S['sig_value'])],
                [Paragraph('代表取締役　前田 敦也　　　㊞', S['sig_label'])],
            ], colWidths=[75*mm],
               style=TableStyle([
                   ('LINEBELOW', (0,4),(0,4), 0.5, RULE),
               ])),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[85*mm, 85*mm])
    sig_table.setStyle(TableStyle([
        ('VALIGN',  (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING',  (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(sig_table)

    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width='100%', thickness=0.3, color=RULE))
    story.append(Paragraph(
        'このPDFはクラウドサイン登録用です。署名欄は電子署名にて対応してください。',
        S['footer_note']
    ))

    doc.build(story)
    print(f'✓  {OUT}')


if __name__ == '__main__':
    build()
