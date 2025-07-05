import flet as ft
import datetime
from flet import KeyboardType
from google.oauth2.service_account import Credentials
from auto_complemento import get_produto
from googleapiclient.discovery import build

client_json = {
        }

def root(page: ft.Page):
    page.title = "CONTROLE DE QUALIDADE"
    page.bgcolor = "#44b7ec"  # 63a4c8
    page.theme_mode = 'light'
    page.window_maximized = True
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.adaptive = True
    page.update()

    def novo_product_maquina(e):
        def voltar(e):
            stack.controls = [Content]
            page.update()

        def save_new_produto(e):
            global client_json
            # Autenticando
            scopes = ["scopes"]
            creds = Credentials.from_service_account_info(
                client_json, scopes=scopes)
            service = build('sheets', 'v4', credentials=creds)
            sheet_name = 'Aba4'
            spreadsheet_id = 'spreadsheet_id'
            codigo = novo_codigo.value
            nome = novo_produto.value
            if not codigo or not nome:
                page.snackbar = ft.SnackBar(
                    content=ft.Text("Preencha código e nome!"),
                    bgcolor=ft.colors.RED,
                    behavior=ft.SnackBarBehavior.FLOATING
                )
            else:
                novos_dados = [[codigo,nome]]
                body = {'values': novos_dados}
                # Append data na planilha
                service.spreadsheets().values().append(
                    spreadsheetId=spreadsheet_id,
                    range=f"{sheet_name}!A1",
                    valueInputOption="RAW",
                    body=body
                ).execute()
                page.snackbar = ft.SnackBar(
                    content=ft.Text(f"Produto '{nome}' ({codigo}) salvo!"),
                    bgcolor=ft.colors.GREEN,
                    behavior=ft.SnackBarBehavior.FLOATING,
                    duration=2000
                )
                #limpar campos
                novo_codigo.value = ""
                novo_produto.value = ""

            page.open(page.snackbar)
            page.update()

        novo_produdo_maquina = ft.Container(
            border_radius=12,
            expand=True,
            gradient=ft.LinearGradient(
                colors=["#6f56d0", "#5feee3"],  # 5feee3
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center
            ),
            alignment=ft.alignment.center,
            content=ft.Text('ADICIONAR NOVO PRODUTO/MAQUINA', size=40,
                            color='white', theme_style=ft.TextThemeStyle.LABEL_MEDIUM)
        )
        novo_codigo = ft.TextField(label="numero do codigo", filled=True)
        novo_produto = ft.TextField(label="nome do produto", filled=True)
        P_M_BUTTOM = ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_BACK,
                              icon_color="BLUE", on_click=voltar),
                ft.ElevatedButton("SALVAR", color="BLUE",
                                  on_click=save_new_produto)
            ]
        )
        P_M_COLUNA = ft.Column(
            controls=[
                novo_produdo_maquina,
                novo_codigo,
                novo_produto,
                P_M_BUTTOM
            ]
        )
        P_M_CONTEINER = ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            width=9000,
            height=740,
            bgcolor='#F6F6F6FF',
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=3, color='black'),
            content=P_M_COLUNA,
            padding=20,
        )
        stack.controls = [P_M_CONTEINER]
        page.update()

    def formatar_peso(valor: str) -> str:
        digits = ''.join(filter(str.isdigit, valor))
        if not digits:
            return ""
        if len(digits) <= 2:
            int_part = "0"
            dec_part = digits.lstrip("0") or "0"
        else:
            int_part = digits[:-2]
            dec_part = digits[-2:]
        return f"{int(int_part)},{dec_part}"

    # Funções de callback para outros widgets
    def coluna_analisada_change(e):
        # e.control.value é o valor do Radio selecionado
        if e.control.value == "DIGITAR VALOR":
            valor.disabled = False
        else:
            valor.disabled = True
            valor.value = ""  # opcional: limpa o texto quando desabilita
        page.update()

    def peso_change(e):
        e.control.value = formatar_peso(e.control.value)
        page.update()

    def resultado_change(e):
        resultado_dropdow.value = e.control.value
        page.update()

    def Status_de_maquinas_change(e):
        Status_de_maquinas_dropdow.value = e.control.value
        # desabilita resultado_dropdow se PARADO, caso contrário habilita
        resultado_dropdow.disabled = (e.control.value == "PARADO")
        if resultado_dropdow.disabled:
            resultado_dropdow.value = None
        page.update()

    def maquina_change(e):
        maquina_dropbox.value = e.control.value
        page.update()

    def turma_change(e):
        turma_dropdow.value = e.control.value
        page.update()

     # Variáveis para armazenar data e hora selecionadas
    data_escolhida = None
    hora_escolhida = None

    def Hora(e):
        nonlocal hora_escolhida
        hora_escolhida = e.control.value

        horario.value = hora_escolhida.strftime('%H:%M')
        page.update()

    def Data(e):
        nonlocal data_escolhida
        data_escolhida = e.control.value  # Armazena a data escolhida
        # Atualiza o campo de texto "data" para mostrar a data selecionada
        data.value = data_escolhida.strftime('%d/%m/%Y')
        page.update()

     # Função para tratar a seleção do AutoComplete
    def on_maquina_select(e):
        if hasattr(e.selection, "value"):
            Maquina.value = e.selection.value
        else:
            Maquina.value = e.selection
        print("Máquina selecionada:", Maquina.value)
        page.update()
    # Callback que preenche o campo Produto automaticamente
    def pesquisar_e_preencher(e: ft.ControlEvent, page: ft.Page):
        pdt_cg = e.control.value
        pdt = get_produto(pdt_cg)
        if pdt:
            Produto.value = pdt
        else:
            Produto.value = "Produto não encontrado"
        page.update()
    def funcion_enviar(e):
        # Dados da conta de serviço
        global client_json
        
        # Autenticando
        scopes = ["scopes"]
        creds = Credentials.from_service_account_info(
            client_json, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)

        # Referência da Planilha
        if escolher_Widgets.value == "Ensaio de Resistência ao Impacto":
            sheet_name = 'Aba2'
            spreadsheet_id = 'spreadsheet_id'
            # Formatação dos valores de peso e espessuras
            peso_formatado = formatar_peso(Peso.value)
            cp_vals = []
            formatted_cps = []

            for field in (CP1, CP2, CP3, CP4, CP5, CP6):
                val = formatar_peso(field.value)
                formatted_cps.append(val)
                try:
                    # Converte "12,34" para float
                    cp_vals.append(float(val.replace(',', '.')))
                except:
                    # Ignora valores vazios ou inválidos
                    pass

            # Cálculo da média (Media)
            media_val = sum(cp_vals) / len(cp_vals) if cp_vals else 0
            media_str = f"{media_val:.2f}".replace('.', ',')

            # Lista de switches, na mesma ordem das linhas L1, L2, …
            switches = [S1, S2, S3, S4, S5, S6]

            # Pega o valor digitado em total_de_cp_entry (número de CPs a considerar)
            try:
                total = int(total_de_cp_entry.value)
            except (ValueError, TypeError):
                # se não for número válido, considera todos
                total = len(switches)

            # Garante que 'total' não seja maior que a quantidade de switches disponíveis
            total = min(total, len(switches))

            # Conta quantos switches estão ligados
            selected_count = sum(1 for sw in switches[:total] if sw.value)
            # O resto é o número de CPs não selecionados
            unselected_count = total - selected_count
            # Define status: aprovado se houver pelo menos um selecionado
            status = "APROVADO" if selected_count > 0 else "REPROVADO"
            # Coletando os dados dos widgets Content2
            Z0 = data.value
            Z1 = horario.value
            Z2 = turma_dropdow.value
            Z3 = Responavel.value
            Z4 = maquina_dropbox.value
            Z5 = Codigo.value
            Z6 = Produto.value
            Z7 = n_molde.value
            Z8 = peso_formatado
            Z9 = total_de_cp_entry.value
            Z10, Z11, Z12, Z13, Z14, Z15 = formatted_cps
            Z16 = media_str
            Z17 = selected_count
            Z18 = unselected_count
            Z19 = status
            novos_dados = [[Z0, Z1, Z2, Z3, Z4, Z5, Z6, Z7,
                            Z8, Z9, Z10, Z11, Z12, Z13, Z14, Z15, Z16, Z17, Z18, Z19]]
            body = {'values': novos_dados}
            # Append data na planilha
            service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=f"{sheet_name}!A1",
                valueInputOption="RAW",
                body=body
            ).execute()
        elif escolher_Widgets.value == "Controle de Bolachas e Fichas":
            sheet_name = 'Aba 3'
            spreadsheet_id = 'spreadsheet_id'
            X0 = data.value
            X1 = turma_dropdow.value
            X2 = horario.value
            X3 = Responavel.value
            X4 = maquina_dropbox.value
            X5 = Codigo.value
            X6 = Produto.value
            X7 = coletadas.value
            if coluna_analisada.value == "TUDO":
                X8 = coletadas.value
            else:
                X8 = valor.value
            X9 = obs.value

            novos_dados = [[X0, X1, X2, X3, X4,
                            X5, X6, X7, X8, "", "", X9]]
            body = {'values': novos_dados}
            # Append data na planilha
            service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=f"{sheet_name}!A1",
                valueInputOption="RAW",
                body=body
            ).execute()
        else:
            sheet_name = 'Aba1'
            spreadsheet_id = 'spreadsheet_id' #1UN7MffDuS_V4oc2ccNszm5gFYkjd1a-JKDEZSRcyjFk

            # Coletando os dados dos widgets Content
            T0 = data.value
            T1 = horario.value
            T2 = turma_dropdow.value
            T3 = Responavel.value
            T4 = maquina_dropbox.value
            T5 = Codigo.value
            T6 = Produto.value
            T7 = Status_de_maquinas_dropdow.value
            T8 = resultado_dropdow.value
            T9 = seleção_Operador_realizou.value

            novos_dados = [[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9]]
            body = {'values': novos_dados}

            # Append data na planilha
            service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=f"{sheet_name}!A1",
                valueInputOption="RAW",
                body=body
            ).execute()

        # Limpar campos após envio
        data.value = ""
        horario.value = ""
        turma_dropdow.value = None
        turma_dropdow.value = "empty"
        Responavel.value = ""
        maquina_dropbox.value = "empty"
        Codigo.value = ""
        Produto.value = ""
        Status_de_maquinas_dropdow.value = None
        Status_de_maquinas_dropdow.value = "empty"
        resultado_dropdow.value = None
        resultado_dropdow.value = "empty"
        seleção_Operador_realizou.value = None
        n_molde.value = ""
        Peso.value = None
        total_de_cp_text.value = ""
        CP1.value = None
        CP2.value = None
        CP3.value = None
        CP4.value = None
        CP5.value = None
        CP6.value = None
        S1.value = None
        S2.value = None
        S3.value = None
        S4.value = None
        S5.value = None
        S6.value = None
        coletadas.value = ""
        coluna_analisada.value = None
        valor.value = ""
        obs.value = ""

        # Mostrar SnackBar de sucesso
        page.open(ft.SnackBar(
            content=ft.Text("Dados enviados com sucesso!"),
            bgcolor=ft.colors.GREEN,
            behavior=ft.SnackBarBehavior.FLOATING,
            show_close_icon=True,
            duration=2000
        )
        )
        page.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.EMAIL,
        bgcolor='BLUE',
        on_click=funcion_enviar,
        tooltip="Enviar"
    )

    end_drawer = ft.NavigationDrawer(
        position=ft.NavigationDrawerPosition.END,
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP, label="Rotomoldagem"),
            ft.NavigationDrawerDestination(icon=ft.Icon(
                ft.Icons.ADD_COMMENT), label="Item 2"),
            ft.NavigationDrawerDestination(icon=ft.Icon(
                ft.Icons.ADD_COMMENT), label="Item 3"),
            ft.NavigationDrawerDestination(icon=ft.Icon(
                ft.Icons.ADD_COMMENT), label="Item 4"),
        ],
    )

    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor='#F6F6F6FF',
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.BLUE,
                              icon_size=28, on_click=lambda e: page.open(end_drawer), tooltip="Menu"),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.ADD,
                              icon_color=ft.Colors.BLUE, icon_size=28, on_click=novo_product_maquina, tooltip="Adicionar novo Produto/Maquina"),
            ]
        ),
    )

    # Campos de entrada Ensaio de Desplacamento da Pintura UV
    data = ft.TextField(label='Data')
    horario = ft.TextField(label='Horario')
    Responavel = ft.TextField(label='Responsavel')
    maquina_dropbox = ft.Dropdown(
        label="maquina",
        options=[
            ft.dropdown.Option("Ferry 1"),
            ft.dropdown.Option("Ferry 2"),
            ft.dropdown.Option("Ferry 3"),
            ft.dropdown.Option("Ferry 4"),
            ft.dropdown.Option("Ferry 5"),
            ft.dropdown.Option("Rotoline 1"),
            ft.dropdown.Option("Rotoline 2"),
            ft.dropdown.Option("Rotoline 3"),
            ft.dropdown.Option("Rotoline 4"),
            ft.dropdown.Option("Rotoline 5"),
            ft.dropdown.Option("Rotoline 6"),
            ft.dropdown.Option("Rotoline 7"),
            ft.dropdown.Option("Haitian 300"),
            ft.dropdown.Option(text="\u200B", key="empty")
        ],
        on_change=maquina_change,  # Função que atualiza a seleção
        width=150

    )
    Maquina = ft.AutoComplete(

        suggestions=[
            ft.AutoCompleteSuggestion(key="ferry ", value="Ferry 1"),
            ft.AutoCompleteSuggestion(key="ferry", value="Ferry 2"),
            ft.AutoCompleteSuggestion(key="ferry", value="Ferry 3"),
            ft.AutoCompleteSuggestion(key="ferry", value="Ferry 4"),
            ft.AutoCompleteSuggestion(key="ferry", value="Ferry 5"),
            ft.AutoCompleteSuggestion(key="rotoline ", value="Rotoline 1"),
            ft.AutoCompleteSuggestion(key="rotoline ", value="Rotoline 2"),
            ft.AutoCompleteSuggestion(key="rotoline ", value="Rotoline 3"),
            ft.AutoCompleteSuggestion(key="rotoline ", value="Rotoline 4"),
            ft.AutoCompleteSuggestion(key="rotoline ", value="Rotoline 5"),
            ft.AutoCompleteSuggestion(key="rotoline ", value="Rotoline 6"),
            ft.AutoCompleteSuggestion(key="rotoline ", value="Rotoline 7"),
            ft.AutoCompleteSuggestion(key="haitian 300 ", value="Haitian 300"),
        ],
        on_select=on_maquina_select
    )
    Codigo = ft.TextField(
        label='Codigo', on_submit=lambda e: pesquisar_e_preencher(e, page), width=140, keyboard_type=KeyboardType.NUMBER,) #on_change=on_codigo_change
    Produto = ft.TextField(label='Produto', width=380)
    Text_Operador_realizou = ft.Text('Operador Realizou?', size=15)
    titulo = ft.Text('Ensaio de Desplacamento da Pintura UV', size=40,
                     color='white', theme_style=ft.TextThemeStyle.LABEL_MEDIUM)

    container_texto = ft.Container(
        border_radius=12,
        expand=True,
        gradient=ft.LinearGradient(
            colors=["#5feee3", "#6f56d0"],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center
        ),
        alignment=ft.alignment.center,
        content=titulo
    )

    # Callback para o DropdownM2 que alterna entre containers
    def dropdown_change(e):
        # Verifica o valor selecionado
        if escolher_Widgets.value == "Ensaio de Resistência ao Impacto":
            stack.controls = [Content2]
        elif escolher_Widgets.value == "Controle de Bolachas e Fichas":
            stack.controls = [Content3]
        else:
            stack.controls = [Content]
        page.update()

    # Mudar de coluna
    escolher_Widgets = ft.DropdownM2(
        label='SERVIÇOS',
        width=300,
        options=[
            ft.dropdownm2.Option("Ensaio de Desplacamento da Pintura UV"),
            ft.dropdownm2.Option("Ensaio de Resistência ao Impacto"),
            ft.dropdownm2.Option("Controle de Bolachas e Fichas"),
        ],
        on_change=dropdown_change
    )

    turma_dropdow = ft.Dropdown(
        label="Turma",
        options=[
            ft.dropdown.Option("A"),
            ft.dropdown.Option("B"),
            ft.dropdown.Option("C"),
            ft.dropdown.Option("D"),
            ft.dropdown.Option(text="\u200B", key="empty")
        ],
        on_change=turma_change,  # Função que atualiza a seleção
        width=150

    )

    resultado_dropdow = ft.Dropdown(
        label="Resultado",
        options=[
            ft.dropdown.Option("APROVADO"),
            ft.dropdown.Option("REPROVADO"),
            ft.dropdown.Option(text="\u200B", key="empty")
        ],
        on_change=resultado_change,  # Função que atualiza a seleção
        width=170

    )

    Status_de_maquinas_dropdow = ft.Dropdown(
        label="Status de Maquinas",
        options=[
            ft.dropdown.Option("PRODUZINDO"),
            ft.dropdown.Option("PARADO"),
            ft.dropdown.Option(text="\u200B", key="empty")
        ],
        on_change=Status_de_maquinas_change,  # Função que atualiza a seleção
        width=220

    )

    seleção_Operador_realizou = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="SIM", label="SIM"),
        ft.Radio(value="NÃO", label="NÃO"),
    ]))

    # Relogio
    relogio = ft.TimePicker(
        confirm_text="Confirmar",
        cancel_text='Cancelar',
        error_invalid_text="Horario Incorreto",
        help_text="Horario de Chegada",
        on_change=Hora
    )
    # botado Relogio
    botao_relogio = ft.ElevatedButton(
        "Horario",
        color='BLUE',
        icon=ft.Icons.TIMER,
        icon_color=ft.Colors.BLUE,
        on_click=lambda _: page.open(relogio),
    )
    # Botao Hora e Data
    H_D = ft.Row(

        controls=[

            # turma_dropdow, computador
            botao_relogio,
            ft.ElevatedButton(
                "Data",
                color='BLUE',
                icon=ft.Icons.CALENDAR_MONTH,
                icon_color=ft.Colors.BLUE,
                on_click=lambda e: page.open(
                    ft.DatePicker(
                        first_date=datetime.datetime(
                            year=1900, month=1, day=1),
                        last_date=datetime.datetime(
                            year=7200, month=12, day=31),
                        on_change=Data,
                    )
                ),
            ),
        ]
    )
    # computador
    C_P = ft.Row(
        controls=[
            Codigo,
            Produto
        ]
    )
    C1 = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            container_texto,
            escolher_Widgets,
            Responavel,
            H_D,
            turma_dropdow,
            maquina_dropbox,
            Codigo,
            Produto,
            Status_de_maquinas_dropdow,
            resultado_dropdow,
            Text_Operador_realizou,
            seleção_Operador_realizou
        ],
    )

    Lista = ft.ListView(
        width=9000,
        height=740,
        controls=[C1]
    )

    # Campo de entrada Ensaio de Resistência ao Impacto
    titulo2 = ft.Text('Ensaio de Resistência ao Impacto', size=40,
                      color='white', theme_style=ft.TextThemeStyle.LABEL_MEDIUM)
    container_texto2 = ft.Container(
        alignment=ft.alignment.center,
        border_radius=12,
        expand=True,
        gradient=ft.LinearGradient(
            colors=["#5feee3", "#6f56d0"],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center
        ),
        content=titulo2
    )
    n_molde = ft.TextField(label="N° do Molde", width=100,
                           keyboard_type=KeyboardType.NUMBER,)
    Peso = ft.TextField(label="Peso(Kg)",
                        border=ft.InputBorder.NONE,
                        filled=True,
                        hint_text="Não Utilize Pontos ou Virgulas",
                        on_change=peso_change,
                        keyboard_type=KeyboardType.NUMBER,
                        )
    total_de_cp_text = ft.Text("Total de CP:", size=15)
    total_de_cp_entry = ft.TextField(width=60)
    CP1 = ft.TextField(label="ESPESSURA CP 01",
                       border=ft.InputBorder.NONE,
                       filled=True,
                       hint_text="Não Utilize Pontos ou Virgulas",
                       on_change=peso_change,
                       keyboard_type=KeyboardType.NUMBER,
                       )
    CP2 = ft.TextField(label="ESPESSURA CP 02",
                       border=ft.InputBorder.NONE,
                       filled=True,
                       hint_text="Não Utilize Pontos ou Virgulas",
                       on_change=peso_change,
                       keyboard_type=KeyboardType.NUMBER,
                       )
    CP3 = ft.TextField(label="ESPESSURA CP 03",
                       border=ft.InputBorder.NONE,
                       filled=True,
                       hint_text="Não Utilize Pontos ou Virgulas",
                       on_change=peso_change,
                       keyboard_type=KeyboardType.NUMBER,
                       )
    CP4 = ft.TextField(label="ESPESSURA CP 04",
                       border=ft.InputBorder.NONE,
                       filled=True,
                       hint_text="Não Utilize Pontos ou Virgulas",
                       on_change=peso_change,
                       keyboard_type=KeyboardType.NUMBER,
                       )
    CP5 = ft.TextField(label="ESPESSURA CP 05",
                       border=ft.InputBorder.NONE,
                       filled=True,
                       hint_text="Não Utilize Pontos ou Virgulas",
                       on_change=peso_change,
                       keyboard_type=KeyboardType.NUMBER,
                       )
    CP6 = ft.TextField(label="ESPESSURA CP 06",
                       border=ft.InputBorder.NONE,
                       filled=True,
                       hint_text="Não Utilize Pontos ou Virgulas",
                       on_change=peso_change,
                       keyboard_type=KeyboardType.NUMBER,
                       )
    # Switch Windgets
    S1 = ft.Switch(adaptive=True, label="APROVADO", value='1')
    S2 = ft.Switch(adaptive=True, label="APROVADO", value='1')
    S3 = ft.Switch(adaptive=True, label="APROVADO", value='1')
    S4 = ft.Switch(adaptive=True, label="APROVADO", value='1')
    S5 = ft.Switch(adaptive=True, label="APROVADO", value='1')
    S6 = ft.Switch(adaptive=True, label="APROVADO", value='1')
    # linhas dos Slider e TextField
    L1 = ft.Row(controls=[CP1, S1,])
    L2 = ft.Row(controls=[CP2, S2])
    L3 = ft.Row(controls=[CP3, S3])
    L4 = ft.Row(controls=[CP4, S4])
    L5 = ft.Row(controls=[CP5, S5])
    L6 = ft.Row(controls=[CP6, S6])
    R_total_de_cp = ft.Row(controls=[total_de_cp_text, total_de_cp_entry])
    # Coluna 2
    C2 = ft.Column(
        controls=[
            container_texto2,
            escolher_Widgets,
            Responavel,
            H_D,
            turma_dropdow,
            maquina_dropbox,
            Codigo,
            Produto,
            n_molde,
            Peso,
            # total_de_cp_text,
            # total_de_cp_slider,
            R_total_de_cp,
            L1,
            L2,
            L3,
            L4,
            L5,
            L6,
        ]
    )

    Lista2 = ft.ListView(
        width=9000,
        height=740,
        controls=[C2]
    )

    Content2 = ft.Container(
        width=9000,  # 9000
        height=740,  # 740
        bgcolor='#F6F6F6FF',
        expand=True,
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=3, color='black'),
        content=Lista2,
        alignment=ft.alignment.center,
        padding=20,
    )
    # Campo de entrada Controle de Bolachas e Fichas
    titulo3 = ft.Text('Controle de Bolachas e Fichas', size=40,
                      color='white', theme_style=ft.TextThemeStyle.LABEL_MEDIUM)
    container_texto3 = ft.Container(
        alignment=ft.alignment.center,
        border_radius=12,
        expand=True,
        gradient=ft.LinearGradient(
            colors=["#5feee3", "#6f56d0"],
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center
        ),
        content=titulo3
    )
    coletadas = ft.TextField(width=60, filled=True,
                             keyboard_type=KeyboardType.NUMBER)
    text_coletadas = ft.Text("BOLACHAS COLETADAS:", size=13, color='#919396')
    ROW_COLETADAS = ft.Row(
        controls=[
            text_coletadas,
            coletadas
        ]
    )
    text_analisada = ft.Text('BOLACHAS ANALISADAS:')
    valor = ft.TextField(width=60, filled=True, disabled=True,
                         keyboard_type=KeyboardType.NUMBER)

    coluna_analisada = ft.RadioGroup(
        content=ft.Column([
            text_analisada,
            ft.Radio(value="TUDO", label="TODAS"),
            ft.Row(
                controls=[ft.Radio(value="DIGITAR VALOR", label="DIGITAR VALOR:"),
                          valor
                          ]
            )
        ]
        ),
        on_change=coluna_analisada_change
    )
    obs = ft.TextField(
        label="OBS.:",
        multiline=True,
        min_lines=1,
        max_lines=3,
    )
    C3 = ft.Column(
        controls=[
            container_texto3,
            escolher_Widgets,
            Responavel,
            H_D,
            turma_dropdow,
            maquina_dropbox,
            Codigo,
            Produto,
            ROW_COLETADAS,
            coluna_analisada,
            obs
        ]
    )

    Lista3 = ft.ListView(
        width=9000,
        height=740,
        controls=[C3]
    )

    Content3 = ft.Container(
        width=9000,  # 9000
        height=740,  # 740
        bgcolor='#F6F6F6FF',
        expand=True,
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=3, color='black'),
        content=Lista3,
        alignment=ft.alignment.center,
        padding=20,
    )

    Content = ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        width=9000,
        height=740,
        bgcolor='#F6F6F6FF',
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=3, color='black'),
        content=Lista,
        padding=20,
    )

    stack = ft.Stack(
        alignment=ft.alignment.center,
        expand=True,
        controls=[
            Content,
        ]
    )

    page.add(stack)


ft.app(target=root)
