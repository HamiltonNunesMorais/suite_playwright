@echo off
REM Criar ambiente virtual
python -m venv venv

REM Ativar ambiente virtual
call venv\Scripts\activate

REM Atualizar pip
python -m pip install --upgrade pip

REM Instalar dependências do requirements.txt
pip install -r requirements.txt

REM Instalar Playwright (caso não esteja listado no requirements.txt)
pip install playwright

REM Instalar navegadores necessários para Playwright
playwright install

echo Ambiente configurado com sucesso!
pause
