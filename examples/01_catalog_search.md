# Catalog search with price filter and recommendation

Real conversation with the agent (model `gemini-3.5-flash`, 2026-11-02 20:25). Lines starting with `tool` show the functions the agent called.

**Customer:** Oi! Quais opções de violões disponíveis custando até R$1000?

> tool: `search_products({'max_price': 1000, 'category': 'Violões', 'only_available': True})`
> tool: `get_active_promotions({'category': 'Violões'})`

**Agent:** Olá! Temos ótimas opções de violões disponíveis em nosso estoque até R$ 1.000,00. Confira a lista:

**Opções com Cordas de Nylon:**
- **Tagima Memphis AC-39 Nylon Natural** — R$ 429,90
- **Rozini RC-104 Nylon Estudante** — R$ 459,90
- **Yamaha C40 Nylon Natural** — R$ 599,90
- **Giannini GN-15 Nylon Cedr Natural** — R$ 689,00
- **Yamaha C70 Nylon Natural** — R$ 849,00

**Opções com Cordas de Aço:**
- **Shelby SN-100 Folk Aço Preto** — R$ 549,00
- **Giannini GF-1R Aço Folk Sunburst** — R$ 579,90
- **Yamaha F310 Aço Natural** — R$ 699,90
- **Tagima Dallas Tuner Aço Natural** — R$ 749,00
- **Shelby SGD-195E Elétrico Aço Sunburst** — R$ 799,00
- **Tagima Woodstock Dreadnought Natural** — R$ 899,00
- **Tagima TW-7 (7 Cordas) Aço Natural** — R$ 999,00

Lembrando que para pagamentos à vista via **PIX** você garante **5% de desconto**, ou pode parcelar em até **12x sem juros** no cartão de crédito!

Algum desses modelos chamou sua atenção? Se quiser saber mais detalhes sobre qualquer um deles, é só me avisar!

---

**Customer:** Sou iniciante e queria um de aço. Qual você recomenda?

> tool: `get_product_details({'product_id': 87})`
> tool: `get_product_details({'product_id': 86})`

**Agent:** Para quem está começando no violão de aço, recomendo principalmente dois modelos que se destacam muito pelo conforto, tocabilidade e excelente custo-benefício:

1. **Yamaha F310 Aço Natural — R$ 699,90**
   - **Por que recomendo:** É um dos violões mais vendidos e recomendados do mundo para iniciantes. A Yamaha tem um controle de qualidade incrível, o braço é muito confortável e o timbre é bem encorpado e equilibrado. É um instrumento durável que vai te acompanhar por anos.

2. **Tagima Dallas Tuner Aço Natural — R$ 749,00**
   - **Por que recomendo:** Um grande diferencial para quem está aprendendo é que ele já vem com **afinador integrado** no próprio instrumento. Isso facilita demais na hora de praticar sem precisar de aplicativos no celular. Tem corpo confortável e som brilhante.

Se você procura praticidade na hora de afinar, o **Tagima Dallas** é uma ótima escolha. Se prefere um modelo acústico clássico com acabamento e durabilidade impecáveis, o **Yamaha F310** é imbatível!

Lembrando que no **PIX** você tem **5% de desconto** (o Yamaha F310 sai por R$ 664,91 e o Tagima Dallas por R$ 711,55) ou dá para parcelar em até **12x sem juros**.

Gostou de algum deles ou gostaria de tirar mais dúvidas?

