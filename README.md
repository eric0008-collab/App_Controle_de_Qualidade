# App_Controle_de_Qualidade
**Enviando dados:**
> Para que os envios dos dados funcione corretamente
> para o dashboard Power bi voce precisa antes enviar os dados para uma
> planilha do [Google Sheets](https://docs.google.com/spreadsheets/u/0/)
> e de lá você integra os dados da sua planilha Google Sheets ao dashboard Power bi
## Integrando o aplicativo a planilha google Sheets
> Para enviar os Dados o aplicativo para o Google Sheets você precisará:
- [x] Instalar as Bibliotecas: google-auth, google-auth-oauthlib e google-api-python-client
- [x] criar um projeto no [Google Cloud Consola](https://cloud.google.com/)
- [x] Ativar as apis do Google Sheets e google driver
- [x] Criar uma Conta de Serviço
- [x] Baixar a Chave.json
- [x] Copiar o email da conta de serviço     
## Ativando API
> Após criar um projeto no Google Cloud clicando na Aba _APIs & Services_
> na barra de pesquisa procure por api google sheets e abilite a api
> faça a mesma coisa com a api do google driver

![api google sheets](https://github.com/user-attachments/assets/8b22531d-671b-4a7e-8280-a626b00a9f71)
![Api google driver](https://github.com/user-attachments/assets/d1ddf74c-a76d-457e-8edf-ee0208faa9af)

> Em seguida na aba _IAM & Admin_ e em _Service Accounts voce cria uma conta de serviço _create service accounts_:
![conta serviço](https://github.com/user-attachments/assets/b97eff4a-7793-4529-8a82-af8c959c994a)
> _OBS:você so precisa criar o nome para sua conta o resto das aplcações vc so confirma_
> 
**Criando chave.json**
>Apos criar a conta de serviço voce baixa a chave.json
>e copia o email de serviço
## Fazendo tudo funcionar!
> Na sua planilha google sheets va em _Arquivo_, _compartilhar_ e cole o email de serviço no campo adicionar participante é muito importe que vc defina a permissão como editor para nosso email editar a planilha
>
> Cole as informaçoes da sua chave.json no campo vazio:
```
  def funcion_enviar(e):
      # Dados da conta de serviço
      client_json = {
          #CHAVE JSON
      }
```
>Em seguida mude o spreadsheet_id para o id da sua planilha do google Sheets pois ela é quem fara a integração do aplicativo para a aba ao qual vc quer editar
>
>O spreadsheet_id da sua planilha fica na URL da sua planilha sheets entre "/d/" e "/edit"
>
>Exemplo _https://docs.google.com/spreadsheets/d/_ **spreadsheet_id** _/edit?gid=0#gid=0_
>
>Copie e cole no lugar de **'spreadsheet_id'**
>e mude 'Aba1'para o nome da aba ao qual vc quer trabalhar
>
>Faça isso em todas as sheet_name e spreadsheet_id que estiverem no codigo
```
if escolher_Widgets.value == "Ensaio de Resistência ao Impacto":
            sheet_name = 'Aba1'
            spreadsheet_id = 'spreadsheet_id'
```
>fazendo isso vc conseguirar enviar dados do aplicativo para o Google Sheets
## Integrando o google sheets ao Power bi
>Para integrar o Google Sheets ao Power Bi vc so precisa copiar a URL da sua planilha e no power bi va em _Obter outros dados e fonte_ e no campo de pesquisa que aparecer digite Google Planilhas
>
>Selecione a opção que aparecer e cole a URL que vc copiou, por segurança ele ira pedir o email que vc usou para acessar o google sheets é so logar e digitar a senha e pronto vc tera todos os dados da sua planilha automatizada
**Obs: importante tratar os dados antes de criar o dashboard**


