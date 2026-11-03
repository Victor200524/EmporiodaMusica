# Price lookup, expired promotion and discontinued product

Real conversation with the agent (model `gemini-3.5-flash`, 2026-11-02 20:25). Lines starting with `tool` show the functions the agent called.

**Customer:** Quanto custa o Takamine GD20?

> tool: `search_products({'only_available': False, 'query': 'Takamine GD20'})`
> tool: `get_product_details({'product_id': 95})`

**Agent:** O violão **Takamine GD20 Dreadnought Natural** está saindo por **R$ 2.199,00**.

Temos ele disponível em estoque! Aqui estão as condições de pagamento:
- **PIX (com 5% de desconto):** R$ 2.089,05
- **Cartão de crédito:** Até 12x sem juros de R$ 183,25

Precisa de mais alguma informação sobre esse modelo ou deseja garantir o seu?

---

**Customer:** Vi que ele estava na Oferta Especial, ainda está valendo?

**Agent:** A promoção **Oferta Especial** para o Takamine GD20 infelizmente já encerrou e não está mais ativa.

O valor atual dele é o preço de tabela de **R$ 2.199,00**. 

Mas você ainda pode aproveitar **5% de desconto no PIX**, ficando por **R$ 2.089,05**, ou parcelar em até **12x sem juros de R$ 183,25** no cartão de crédito.

Posso te ajudar com mais alguma dúvida sobre ele?

---

**Customer:** E o Shelby SN-7C, vocês têm?

> tool: `search_products({'only_available': False, 'query': 'Shelby SN-7C'})`
> tool: `search_products({'only_available': True, 'query': '7 cordas', 'category': 'Violões'})`

**Agent:** O modelo **Shelby SN-7C** foi descontinuado pelo fabricante e não faz mais parte do nosso catálogo.

Como você está procurando um violão de 7 cordas de nylon, tenho ótimas opções semelhantes disponíveis em estoque:

* **Giannini GWNE-7 7 Cordas Nylon Natural:** R$ 1.149,00 *(ou R$ 1.091,55 no PIX)*
* **Rozini RV-174 7 Cordas Nylon Natural:** R$ 1.299,00 *(ou R$ 1.234,05 no PIX)*

Se aceitar opção com cordas de aço, também temos:
* **Tagima TW-7 7 Cordas Aço Natural:** R$ 999,00 *(ou R$ 949,05 no PIX)*

Gostaria de ver os detalhes de algum desses modelos?

