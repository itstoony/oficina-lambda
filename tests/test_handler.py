import pytest
from unittest.mock import patch, MagicMock
from src.handler import validar_cpf, lambda_handler


class TestValidarCPF:
    def test_cpf_valido(self):
        assert validar_cpf("529.982.247-25") is True

    def test_cpf_valido_sem_formatacao(self):
        assert validar_cpf("52998224725") is True

    def test_cpf_invalido_digitos_verificadores(self):
        assert validar_cpf("123.456.789-00") is False

    def test_cpf_todos_iguais(self):
        assert validar_cpf("111.111.111-11") is False

    def test_cpf_tamanho_errado(self):
        assert validar_cpf("123") is False

    def test_cpf_vazio(self):
        assert validar_cpf("") is False


class TestLambdaHandler:
    def test_sem_cpf_retorna_400(self):
        event = {"body": "{}"}
        resultado = lambda_handler(event, None)
        assert resultado["statusCode"] == 400

    def test_cpf_invalido_retorna_400(self):
        event = {"body": '{"cpf": "111.111.111-11"}'}
        resultado = lambda_handler(event, None)
        assert resultado["statusCode"] == 400

    @patch("src.handler.buscar_cliente")
    def test_cliente_nao_encontrado_retorna_404(self, mock_buscar):
        mock_buscar.return_value = None
        event = {"body": '{"cpf": "529.982.247-25"}'}
        resultado = lambda_handler(event, None)
        assert resultado["statusCode"] == 404

    @patch("src.handler.gerar_token")
    @patch("src.handler.buscar_cliente")
    def test_autenticacao_bem_sucedida(self, mock_buscar, mock_token):
        mock_buscar.return_value = {
            "id": "uuid-123",
            "nome": "Tony Silva",
            "email": "tony@email.com"
        }
        mock_token.return_value = "eyJ.token.jwt"
        event = {"body": '{"cpf": "529.982.247-25"}'}
        resultado = lambda_handler(event, None)
        assert resultado["statusCode"] == 200
