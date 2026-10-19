import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
from io import BytesIO

# ---------------------- CONFIGURAÇÃO ----------------------
st.set_page_config(
    page_title="Dashboard RH — Headcount Completo",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- DADOS ----------------------
dados_empregados = """
MAT|NOME|ASO|ADMISSÃO|VENCIMENTO_CONTRATO|CPF|CATEGORIA|SALARIO_DEZ25|SALARIO_JUL26|CARGO|DEPARTAMENTO|EMPRESA|TELEFONE|EMAIL|LOCAL_TRABALHO
3|ADRIANA NEVES DOS SANTOS|5/11/26|11/3/23|1/31/24|140.966.707-31|EMPREGADO|2687.35|3302.20|ASSISTENTE DE COMPRAS II|COMPRAS|G4 CONSTRUTORA & INCORPORADORA LTDA||adriana.guimaraes@g4incorporadora.com.br|ESCRITÓRIO
19|ARIANE SORIANO JORGE DURUTEU|11/27/25|1/6/25|4/5/25|150.349.817-42|EMPREGADO|2321.00|2425.44|ASSISTENTE DE VENDAS NIVEL I|COMERCIAL|G4 CONSTRUTORA & INCORPORADORA LTDA||ariane.soriano@g4incorporadora.com.br|ESCRITÓRIO
30|BETO GUEDES LEITE|5/21/26|6/11/25|9/8/25|794.714.392-72|EMPREGADO|2934.80|3066.80|PEDREIRO|OPERACIONAL|G4 CONSTRUTORA & INCORPORADORA LTDA|21 99935-2305|beto.guedes@g4incorporadora.com.br|OBRA - MANUTENÇÃO
29|CARLOS ALBERTO SILVA FERREIRA|5/18/26|6/2/25|8/30/25|012.218.237-52|EMPREGADO|2934.80|3066.80|PINTOR DE OBRAS|OPERACIONAL|G4 CONSTRUTORA & INCORPORADORA LTDA|21 99450-6850||OBRA
34|EMELY PINA SANTOS|8/19/26|9/1/25|8/31/25|167.270.807-98|ESTAGIARIO|1150.00|1150.00|ESTAGIÁRIA|RH|G4 CONSTRUTORA & INCORPORADORA LTDA|21 95101-3201||ESCRITÓRIO
23|ENES JOSE FIRMINO|4/16/26|5/5/25|8/2/25|873.485.867-91|EMPREGADO|2934.80|3066.80|PEDREIRO|OPERACIONAL|G4 CONSTRUTORA & INCORPORADORA LTDA|21 97518-9015|enesjose58@gmail.com|OBRA - MANUTENÇÃO
33|EVANDRO SANTOS DA CONCEIÇÃO|8/24/26|9/1/25|11/29/25|137.146.797-82|EMPREGADO|3165.00|3307.42|CHEFE DE DEPÓSITO|OPERACIONAL|G4 CONSTRUTORA & INCORPORADORA LTDA|21 99038-2427||DEPÓSITO
14|FABIO ANTUNES MARINHO|11/27/25|1/6/25|4/5/25|032.171.777-54|EMPREGADO|4054.80|4237.20|ENCARREGADO DE MANUTENÇÃO NIVEL I|OPERACIONAL|PREMOL RJ LTDA|21 97640-3864|fabio.antunes@g4incorporadora.com.br|OBRA - MANUTENÇÃO
1|GABRIELA OLIVEIRA GODINHO|X|X|X|159.196.267-63|CONTRIBUINTE|1621.00|1621.00|SOCIO ADMINISTRATIVO|FINANCEIRO|G4 CONSTRUTORA & INCORPORADORA LTDA||gabriela.oliveira@g4incorporadora.com.br|ESCRITÓRIO
1|LEONARDO SANTOS FAGUNDES|10/7/25|10/14/24|1/11/25|176.932.107-17|EMPREGADO|2000.00|2000.00|ASSISTENTE ADMINISTRATIVO|ADMINISTRATIVO|G4 SOLUÇÕES FINANCEIRAS LTDA||leonardo.fagundes@g4incorporadora.com.br|ESCRITÓRIO
3|MARCO ANTONIO FERREIRA ALVES|5/15/26|3/11/24|6/8/24|915.210.417-68|EMPREGADO|2235.20|2336.40|VIGIA|OPERACIONAL|PREMOL RJ LTDA|21 98896-7564||OBRA - SÃO JOÃO
17|MESAQUE ALVARENGA MENDES|5/18/26|5/20/25|8/17/25|169.944.367-05|EMPREGADO|2235.20|2336.40|MEIO OFICIAL|OPERACIONAL|PREMOL RJ LTDA|22 99850-9132||OBRA - BELLA VISTA
4|ROGERIO FERREIRA DOS SANTOS|4/14/26|5/9/25|8/6/25|029.875.877-67|EMPREGADO|2934.80|3066.80|PINTOR DE OBRAS|OPERACIONAL|G4 CONSTRUTORA & INCORPORADORA LTDA|21 97893-7406|rogeriof500@gmail.com|OBRA - MANUTENÇÃO
35|WALACE DE OLIVEIRA CARVALHO|8/24/26|9/24/25|12/22/25|152.180.977-13|EMPREGADO|2120.80|2217.60|SERVENTE|OPERACIONAL|G4 CONSTRUTORA & INCORPORADORA LTDA|21 96881-6345||OBRA - DEPÓSITO
24|WANDERSON SILVA DE OLIVEIRA|1/21/26|5/5/25|8/2/25|182.452.977-55|EMPREGADO|2934.80|3066.80|PEDREIRO|OPERACIONAL|G4 CONSTRUTORA & INCORPORADORA LTDA|21 99041-3159|Wandersomninosilva@gmail.com|OBRA
18|WILSON BRITO FERREIRA|5/15/25|3/18/24|6/15/24|104.945.577-02|EMPREGADO|3471.60|0.00|ALMOXARIFE|OPERACIONAL|PREMOL RJ LTDA|21 98350-1654||OBRA
11|ELIELTON PEREIRA DOS SANTOS|12/29/25|1/5/26|4/4/26|115.369.667-38|EMPREGADO|2934.80|3066.80|PEDREIRO|OPERACIONAL|RESIDENCIAL TOPAZIO SPE LTDA|21 99623-1145||OBRA - MUTUÁ
4|KAUA ARAUJO DOS SANTOS|12/29/25|1/5/26|4/4/26|222.317.017-07|EMPREGADO|2120.80|2217.60|SERVENTE|OPERACIONAL|RESIDENCIAL TOPAZIO SPE LTDA|21 99068-7620||OBRA - MUTUÁ
3|SANDRO DE FREITAS|12/29/25|1/5/26|4/4/26|603.078.923-60|EMPREGADO|4884.00|5104.00|ENCARREGADO DE OBRAS|OPERACIONAL|RESIDENCIAL TOPAZIO SPE LTDA|21 98351-0162||OBRA - MUTUÁ
6|LEONARDO FURTADO DA SILVA BELLO|1/14/26|1/19/26|4/18/26|061.063.717-76|EMPREGADO|2934.80|3066.80|PEDREIRO|OPERACIONAL|RESIDENCIAL TOPAZIO SPE LTDA|21 99655-9643||OBRA - MUTUÁ
12|MARIANA DE PAULA BARROS|1/22/26|3/2/26|5/30/26|163.359.137-98|EMPREGADO|3159.20|3302.20|ASSISTENTE DE ARQUITETURA JUNIOR|ENGENHARIA|G4 CONSTRUTORA & INCORPORADORA LTDA|21 98160-8565|mariana.barros@g4incorporadora.com.br|ESCRITÓRIO
38|EDER BATISTA PEREIRA|1/19/26|3/2/26|5/30/26|847.664.177-04|EMPREGADO|2934.80|3066.80|PEDREIRO|OPERACIONAL|G4 CONSTRUTORA & INCORPORADORA LTDA|21 97552-7430||OBRA - MUTUÁ
8|DEIVID SANTOS DE OLIVEIRA|1/21/26|2/26/26|5/26/26|187.572.687-03|EMPREGADO|2120.80|2217.60|AUXILIAR DE SERVIÇOS GERAIS|OPERACIONAL|RESIDENCIAL TOPAZIO SPE LTDA|21 97460-9863||OBRA - MUTUÁ
1|JHANNA JACKSON MARIA DA SILVA VIDAL|2/20/26|2/23/26|5/23/26|163.285.977-70|EMPREGADO|1750.00|1750.00|ASSISTENTE COMERCIAL|COMERCIAL|MORA SOLUCOES IMOBILIARIAS LTDA|21 98888-7833||ESCRITÓRIO
3|MARIA LUCIA FERREIRA CECIM NETA|3/24/26|3/25/26|6/22/26|187.876.867-08|EMPREGADO|1750.00|1750.00|ASSISTENTE COMERCIAL|COMERCIAL|MORA SOLUCOES IMOBILIARIAS LTDA|21 99459-7340||ESCRITÓRIO
16|LOUISE DOS ANJOS SILVA|3/27/26|4/1/26|6/29/26|169.314.657-67|EMPREGADA|2687.35|2808.28|AUXILIAR DE ENGENHARIA|ENGENHARIA|RESIDENCIAL TOPAZIO SPE LTDA|21 97208-2712|louise.silva@g4incorporadora.com.br|OBRA
40|KELLY OLIVEIRA DO NASCIMENTO NARCIZO DE MELO|4/16/26|4/22/26|7/20/26|136.577.087-74|EMPREGADA|3380.34|3532.45|ASSISTENTE FINANCEIRO PLENO|FINANCEIRO|G4 CONSTRUTORA & INCORPORADORA LTDA|21 97673-3122||ESCRITÓRIO
10|VANDO DIAS MARANHÃO|5/8/26|9/8/26|12/6/26|130.711.517-99|EMPREGADO|2120.80|2217.60|SERVENTE|OPERACIONAL|PORTAL SÃO PEDRO|21 97042-4592||OBRA - MUTUÁ
14|FRANCISCO BEZERRA SILVA|5/18/26|9/8/26|12/6/26|084.570.717-50|EMPREGADO|2934.80|3066.80|PEDREIRO|OPERACIONAL|PORTAL SÃO PEDRO|21 99723-4847||OBRA - MUTUÁ
15|FABIO DOMINGOS DAS NEVES|5/22/26|9/8/26|12/6/26|032.332.227-18|EMPREGADO|2120.80|2217.60|SERVENTE|OPERACIONAL|PORTAL SÃO PEDRO|21 97173-3482||OBRA - MUTUÁ
17|JUAN RAMOS BEZERRA SILVA|5/22/26|9/8/26|12/6/26|213.156.037-05|EMPREGADO|2120.80|2217.60|SERVENTE|OPERACIONAL|PORTAL SÃO PEDRO|21 97029-7535||OBRA - MUTUÁ
16|RENATO DA SILVA BARBOSA|5/22/26|9/8/26|12/6/26|205.187.357-70|EMPREGADO|2120.80|2217.60|SERVENTE|OPERACIONAL|PORTAL SÃO PEDRO|21 96897-8196||OBRA - MUTUÁ
20|JOSUE FAGUNDES DOS SANTOS|5/27/26|9/8/26|12/6/26|962.809.057-72|EMPREGADO|2934.80|3066.80|PEDREIRO|OPERACIONAL|PORTAL SÃO PEDRO|21 98684-3703||OBRA - MUTUÁ
19|CLÁUDIO DE ALENCAR GUERREIRO|5/26/26|9/8/26|12/6/26|077.993.347-89|EMPREGADO|2120.80|2217.60|SERVENTE|OPERACIONAL|PORTAL SÃO PEDRO|21 96673-4467||OBRA - MUTUÁ
18|VALDECI NOIA DA SILVA|5/25/26|9/8/26|12/6/26|000.047.527-08|EMPREGADO|2934.80|3066.80|PEDREIRO|OPERACIONAL|PORTAL SÃO PEDRO|21 97469-8527||OBRA - MUTUÁ
|JULIANA CAMPOS RIBEIRO FERNANDES|6/18/26|6/22/26|9/19/26|056.205.054-05|EMPREGADO|2120.80|2217.60|AUXILIAR DE SERVIÇOS GERAIS|OPERACIONAL|G4 CONSTRUTORA & INCORPORADORA LTDA|21 97067-4101||ESCRITÓRIO
|SAMIRA MENDES DA SILVA|8/11/26|8/12/26|11/9/26|185.866.137-46|EMPREGADO|2000.00|2000.00|ASSISTENTE ADMINISTRATIVO|ADMINISTRATIVO|G4 SOLUÇÕES FINANCEIRAS LTDA|21 98569-7259||ESCRITÓRIO
"""

dados_diretoria = """
NOME|CPF|PAGAMENTO_SOCIO|DATA_NASCIMENTO|EMAIL|TELEFONE
ALEXANDRE DIAS DE ALMEIDA|038.832.817-78|7000.00|5/11/77|alexandre.almeida@g4incorporadora.com.br|
DAVI DA SILVA MIRANDA|156.032.217-98|10000.00|9/29/94|davi.miranda@g4incorporadora.com.br|21 98959-6337
GUILHERME RANGEL DA SILVA|155.591.697-06|7000.00|5/20/93|guilherme.rangel@g4incorporadora.com.br|
GABRIELA OLIVEIRA GODINHO|159.196.267-63|5000.00|6/30/97||
JOACI VIEIRA DE ALMEIDA|306.184.447-34|2000.00|4/25/50|joaci.almeida@g4incorporadora.com.br|
"""

dados_prestadores = """
NOME|CPF|CNPJ|INICIO_CONTRATO|FIM_PRESTACAO|CATEGORIA|VALOR|MENSAGEM|DEPARTAMENTO|SITUACAO|EMPRESA|TELEFONE|LOCAL
GLEISON DE MORAES SOUZA GUIMARÃES|142.141.957-28||||PRESTADOR|7500.00||MARKETING|ATIVO|G4 ORGANIZACOES LTDA||ESCRITÓRIO
PEDRO ANDRE BATISTA BERENGER|128.513.487-79|||PRESTADOR|9000.00|AJUDA CUSTO: 1.158,00|ENGENHARIA|ATIVO|G4 ORGANIZACOES LTDA||ESCRITÓRIO
MAX MARTINS SOUZA|122.314.977-35|||PRESTADOR|3500.00||ENGENHARIA|ATIVO|G4 ORGANIZACOES LTDA||ESCRITÓRIO
MANUELA EVANGELISTA LUZ|127.459.077-94||2/2/26||PRESTADOR|7500.00||RH|ATIVO|G4 ORGANIZACOES LTDA||ESCRITÓRIO
CLAYTON GERMANO LISTA|087.740.947-18||3/4/26||PRESTADOR|6000.00||LEGALIZAÇÃO|ATIVO|G4 ORGANIZACOES LTDA||ESCRITÓRIO
GRAZIELE DA SILVA CESAR|130.957.107-47||3/4/26||PRESTADOR|8000.00||ENGENHARIA|ATIVO|RESIDENCIAL TOPAZIO SPE LTDA||OBRA
VALDECI SIQUEIRA DA SILVA|891.691.827-87||4/1/26||PRESTADOR|6500.00||ENGENHARIA|ATIVO|RESIDENCIAL TOPAZIO SPE LTDA||OBRA
PEDRO MIRA PINHEIRO|152.416.137-30|||PRESTADOR|17000.00||ENGENHARIA|ATIVO|G4 ORGANIZACOES LTDA||ESCRITÓRIO
HITIELLE RANGEL||||PRESTADOR|6800.00||ARQUITETURA|ATIVO|G4 ORGANIZACOES LTDA||ESCRITÓRIO
MARCOS MESAK MENDES|305.816.008-94|||PRESTADOR|8500.00||CONSTRUÇÃO CIVIL|ATIVO|RGD CONSTRUTORA E INCORPORADORA LTDA||OBRA
"""

# ---------------------- FUNÇÕES AUXILIARES ----------------------
def formatar_moeda(valor):
    if pd.isna(valor) or valor == 0: return "—"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def exportar_excel(df, nome_arquivo):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    return output.getvalue()

# ---------------------- CARREGAR DADOS ----------------------
from io import StringIO

# Empregados
df = pd.read_csv(StringIO(dados_empregados), sep="|")
df["SALARIO_DEZ25"] = pd.to_numeric(df["SALARIO_DEZ25"], errors="coerce")
df["SALARIO_JUL26"] = pd.to_numeric(df["SALARIO_JUL26"], errors="coerce")
df["ADMISSÃO"] = pd.to_datetime(df["ADMISSÃO"], errors="coerce")
df["VENCIMENTO_CONTRATO"] = pd.to_datetime(df["VENCIMENTO_CONTRATO"], errors="coerce")
df = df.dropna(subset=["NOME"])
df["AUMENTO_PERC"] = ((df["SALARIO_JUL26"] - df["SALARIO_DEZ25"]) / df["SALARIO_DEZ25"] * 100).round(2)
df["DIFERENCA_VALOR"] = df["SALARIO_JUL26"] - df["SALARIO_DEZ25"]

# Diretoria
df_dir = pd.read_csv(StringIO(dados_diretoria), sep="|")
df_dir["PAGAMENTO_SOCIO"] = pd.to_numeric(df_dir["PAGAMENTO_SOCIO"], errors="coerce")

# Prestadores
df_pj = pd.read_csv(StringIO(dados_prestadores), sep="|")
df_pj["VALOR"] = pd.to_numeric(df_pj["VALOR"], errors="coerce")

# ---------------------- MENU LATERAL ----------------------
pagina = st.sidebar.radio(
    "📑 Navegação",
    ["📊 Visão Geral", "⚠️ Alertas de Vencimento", "💰 Comparativo Salarial", "👔 Diretoria", "🤝 Prestadores PJ"]
)

st.sidebar.divider()
st.sidebar.title("🔍 Filtros")
empresa_filtro = st.sidebar.multiselect("Empresa", sorted(df["EMPRESA"].dropna().unique()))
depto_filtro = st.sidebar.multiselect("Departamento", sorted(df["DEPARTAMENTO"].dropna().unique()))
categoria_filtro = st.sidebar.multiselect("Categoria", sorted(df["CATEGORIA"].dropna().unique()))
local_filtro = st.sidebar.multiselect("Local de Trabalho", sorted(df["LOCAL_TRABALHO"].dropna().unique()))

# Aplicar filtros
df_filtrado = df.copy()
if empresa_filtro: df_filtrado = df_filtrado[df_filtrado["EMPRESA"].isin(empresa_filtro)]
if depto_filtro: df_filtrado = df_filtrado[df_filtrado["DEPARTAMENTO"].isin(depto_filtro)]
if categoria_filtro: df_filtrado = df_filtrado[df_filtrado["CATEGORIA"].isin(categoria_filtro)]
if local_filtro: df_filtrado = df_filtrado[df_filtrado["LOCAL_TRABALHO"].isin(local_filtro)]

hoje = datetime.now()

# ==============================================================
# PÁGINA 1 — VISÃO GERAL
# ==============================================================
if pagina == "📊 Visão Geral":
    st.title("👥 Dashboard de Headcount — G4 & Associadas")
    st.subheader(f"Atualizado em: {hoje.strftime('%d/%m/%Y %H:%M')}")

    # Indicadores
    col1, col2, col3, col4 = st.columns(4)
    total = len(df_filtrado)
    folha = df_filtrado[df_filtrado["SALARIO_JUL26"] > 0]["SALARIO_JUL26"].sum()
    media = df_filtrado[df_filtrado["SALARIO_JUL26"] > 0]["SALARIO_JUL26"].mean()
    empresas = df_filtrado["EMPRESA"].nunique()

    col1.metric("Total Colaboradores", f"{total}")
    col2.metric("Folha Mensal", formatar_moeda(folha))
    col3.metric("Salário Médio", formatar_moeda(media))
    col4.metric("Empresas", f"{empresas}")

    st.divider()

    # Gráficos
    col_a, col_b = st.columns(2)
    depto_cont = df_filtrado["DEPARTAMENTO"].value_counts().reset_index()
    depto_cont.columns = ["Departamento", "Quantidade"]
    fig_depto = px.bar(depto_cont, x="Departamento", y="Quantidade", title="Por Departamento", color="Quantidade", color_continuous_scale="Blues")
    col_a.plotly_chart(fig_depto, use_container_width=True)

    emp_cont = df_filtrado["EMPRESA"].value_counts().reset_index()
    emp_cont.columns = ["Empresa", "Quantidade"]
    fig_emp = px.pie(emp_cont, values="Quantidade", names="Empresa", title="Por Empresa", hole=0.4)
    col_b.plotly_chart(fig_emp, use_container_width=True)

    col_c, col_d = st.columns(2)
    cat_cont = df_filtrado["CATEGORIA"].value_counts().reset_index()
    cat_cont.columns = ["Categoria", "Quantidade"]
    fig_cat = px.pie(cat_cont, values="Quantidade", names="Categoria", title="Tipo de Vínculo", hole=0.3)
    col_c.plotly_chart(fig_cat, use_container_width=True)

    local_cont = df_filtrado["LOCAL_TRABALHO"].value_counts().reset_index()
    local_cont.columns = ["Local", "Quantidade"]
    fig_local = px.bar(local_cont, x="Local", y="Quantidade", title="Por Local", color="Quantidade", color_continuous_scale="Greens")
    col_d.plotly_chart(fig_local, use_container_width=True)

    st.divider()

    # Admissões por mês
    df_filtrado["ANO_MES"] = df_filtrado["ADMISSÃO"].dt.to_period("M").astype(str)
    adm_mes = df_filtrado.groupby("ANO_MES").size().reset_index(name="Admissões")
    fig_adm = px.line(adm_mes, x="ANO_MES", y="Admissões", title="Evolução de Admissões", markers=True)
    st.plotly_chart(fig_adm, use_container_width=True)

    st.divider()

    # Tabela e Exportação
    st.subheader("📋 Lista Completa")
    cols = ["NOME", "CARGO", "DEPARTAMENTO", "EMPRESA", "LOCAL_TRABALHO", "SALARIO_DEZ25", "SALARIO_JUL26", "ADMISSÃO", "TELEFONE"]
    st.dataframe(df_filtrado[cols], use_container_width=True, height=400)

    excel = exportar_excel(df_filtrado[cols], "headcount")
    st.download_button("📥 Exportar para Excel", data=excel, file_name=f"headcount_{hoje.strftime('%Y%m%d')}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Busca
    st.divider()
    st.subheader("🔍 Buscar Colaborador")
    busca = st.text_input("Digite o nome:")
    if busca:
        res = df_filtrado[df_filtrado["NOME"].str.contains(busca.upper(), case=False, na=False)]
        if not res.empty:
            st.dataframe(res.T, use_container_width=True)
        else:
            st.warning("Nenhum resultado encontrado.")

# ==============================================================
# PÁGINA 2 — ALERTAS DE VENCIMENTO
# ==============================================================
elif pagina == "⚠️ Alertas de Vencimento":
    st.title("⚠️ Contratos Próximos do Vencimento")

    # Calcular dias para vencimento
    df_venc = df_filtrado.copy()
    df_venc["DIAS_RESTANTES"] = (df_venc["VENCIMENTO_CONTRATO"] - hoje).dt.days

    # Filtrar válidos
    df_venc = df_venc.dropna(subset=["VENCIMENTO_CONTRATO"])
    df_venc = df_venc[df_venc["VENCIMENTO_CONTRATO"] > datetime(2000, 1, 1)]

    # Classificar
    critico = df_venc[df_venc["DIAS_RESTANTES"] <= 30]
    aviso = df_venc[(df_venc["DIAS_RESTANTES"] > 30) & (df_venc["DIAS_RESTANTES"] <= 90)]
    futuro = df_venc[df_venc["DIAS_RESTANTES"] > 90]

    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 Crítico (≤ 30 dias)", len(critico))
    col2.metric("🟡 Aviso (31–90 dias)", len(aviso))
    col3.metric("🟢 Futuro (> 90 dias)", len(futuro))

    if not critico.empty:
        st.subheader("🔴 Vencem em até 30 dias")
        st.dataframe(critico[["NOME", "CARGO", "VENCIMENTO_CONTRATO", "DIAS_RESTANTES", "EMPRESA"]], use_container_width=True)

    if not aviso.empty:
        st.subheader("🟡 Vencem em 31 a 90 dias")
        st.dataframe(aviso[["NOME", "CARGO", "VENCIMENTO_CONTRATO", "DIAS_RESTANTES", "EMPRESA"]], use_container_width=True)

    if not futuro.empty:
        st.subheader("🟢 Vencem após 90 dias")
        st.dataframe(futuro[["NOME", "CARGO", "VENCIMENTO_CONTRATO", "DIAS_RESTANTES", "EMPRESA"]], use_container_width=True)

    if df_venc.empty:
        st.info("Nenhum vencimento de contrato registrado na planilha.")

    excel = exportar_excel(df_venc, "vencimentos")
    st.download_button("📥 Exportar Vencimentos", data=excel, file_name=f"vencimentos_{hoje.strftime('%Y%m%d')}.xlsx")

# ==============================================================
# PÁGINA 3 — COMPARATIVO SALARIAL
# ==============================================================
elif pagina == "💰 Comparativo Salarial":
    st.title("💰 Evolução Salarial — Dez/25 → Jul/26")

    df_sal = df_filtrado[df_filtrado["SALARIO_DEZ25"] > 0].copy()
    df_sal = df_sal.dropna(subset=["SALARIO_DEZ25", "SALARIO_JUL26"])

    col1, col2, col3 = st.columns(3)
    total_dez = df_sal["SALARIO_DEZ25"].sum()
    total_jul = df_sal["SALARIO_JUL26"].sum()
    var_perc = ((total_jul - total_dez) / total_dez * 100) if total_dez > 0 else 0

    col1.metric("Folha Dez/25", formatar_moeda(total_dez))
    col2.metric("Folha Jul/26", formatar_moeda(total_jul))
    col3.metric("Variação", f"{var_perc:.2f}%")

    st.divider()

    # Gráfico
    fig_comp = px.bar(df_sal.sort_values("DIFERENCA_VALOR", ascending=False),
                      x="NOME", y=["SALARIO_DEZ25", "SALARIO_JUL26"],
                      title="Comparativo Individual", barmode="group",
                      labels={"value": "Salário", "variable": "Período"})
    st.plotly_chart(fig_comp, use_container_width=True)

    # Tabela detalhada
    st.subheader("📋 Detalhamento")
    df_sal["AUMENTO_PERC"] = df_sal["AUMENTO_PERC"].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "—")
    df_sal["DIFERENCA_VALOR"] = df_sal["DIFERENCA_VALOR"].apply(formatar_moeda)
    df_sal["SALARIO_DEZ25"] = df_sal["SALARIO_DEZ25"].apply(formatar_moeda)
    df_sal["SALARIO_JUL26"] = df_sal["SALARIO_JUL26"].apply(formatar_moeda)

    cols_sal = ["NOME", "CARGO", "DEPARTAMENTO", "SALARIO_DEZ25", "SALARIO_JUL26", "DIFERENCA_VALOR", "AUMENTO_PERC"]
    st.dataframe(df_sal[cols_sal], use_container_width=True, height=500)

    excel = exportar_excel(df_sal, "evolucao_salarial")
    st.download_button("📥 Exportar para Excel", data=excel, file_name=f"evolucao_salarial_{hoje.strftime('%Y%m%d')}.xlsx")

# ==============================================================
# PÁGINA 4 — DIRETORIA
# ==============================================================
elif pagina == "👔 Diretoria":
    st.title("👔 Diretoria — Remuneração de Sócios")

    col1, col2 = st.columns(2)
    col1.metric("Total de Diretores", len(df_dir))
    col2.metric("Remuneração Mensal Total", formatar_moeda(df_dir["PAGAMENTO_SOCIO"].sum()))

    st.divider()

    fig_dir = px.bar(df_dir, x="NOME", y="PAGAMENTO_SOCIO", title="Remuneração por Diretor", color="PAGAMENTO_SOCIO")
    st.plotly_chart(fig_dir, use_container_width=True)

    df_dir_exibir = df_dir.copy()
    df_dir_exibir["PAGAMENTO_SOCIO"] = df_dir_exibir["PAGAMENTO_SOCIO"].apply(formatar_moeda)
    st.dataframe(df_dir_exibir, use_container_width=True)

    excel = exportar_excel(df_dir, "diretoria")
    st.download_button("📥 Exportar Diretoria", data=excel, file_name=f"diretoria_{hoje.strftime('%Y%m%d')}.xlsx")

# ==============================================================
# PÁGINA 5 — PRESTADORES PJ
# ==============================================================
elif pagina == "🤝 Prestadores PJ":
    st.title("🤝 Prestadores de Serviço — Pessoa Jurídica")

    col1, col2, col3 = st.columns(3)
    ativos = df_pj[df_pj["SITUACAO"] == "ATIVO"]
    col1.metric("Total Prestadores", len(df_pj))
    col2.metric("Ativos", len(ativos))
    col3.metric("Valor Mensal Total", formatar_moeda(df_pj["VALOR"].sum()))

    st.divider()

    depto_pj = df_pj.groupby("DEPARTAMENTO")["VALOR"].sum().reset_index()
    fig_pj1 = px.pie(depto_pj, values="VALOR", names="DEPARTAMENTO", title="Distribuição por Área")
    st.plotly_chart(fig_pj1, use_container_width=True)

    fig_pj2 = px.bar(df_pj.sort_values("VALOR", ascending=False), x="NOME", y="VALOR", title="Valor por Prestador", color="VALOR")
    st.plotly_chart(fig_pj2, use_container_width=True)

    df_pj_exibir = df_pj.copy()
    df_pj_exibir["VALOR"] = df_pj_exibir["VALOR"].apply(formatar_moeda)
    st.dataframe(df_pj_exibir, use_container_width=True)

    excel = exportar_excel(df_pj, "prestadores_pj")
    st.download_button("📥 Exportar Prestadores", data=excel, file_name=f"prestadores_pj_{hoje.strftime('%Y%m%d')}.xlsx")

# Rodapé
st.sidebar.divider()
st.sidebar.caption(f"G4 & Associadas — Dashboard RH | {hoje.strftime('%d/%m/%Y')}")
