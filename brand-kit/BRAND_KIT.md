# Investidores.vc — Brand Kit (Mini)

> Especificação enxuta para alimentar um agente gerador de **thumbnails de Instagram**.
> Tudo abaixo é a base do design system Deals/Investidores.vc — use como single source of truth.

---

## 1. Identidade visual em 3 frases

- **Marca:** Investidores.vc (apelido interno: **IVC**) — plataforma brasileira de venture capital para investidores.
- **Personalidade:** confiante, premium, calmo, contemporâneo. Não chamativo, não gamificado, não "fintech-genérico".
- **Assinatura visual:** **amarelo** vivo (`#FFBA00`) sobre **near-black** (`#1A1B1F`) ou superfícies brancas/creme. Tipografia geométrica (Cera Pro). Cantos arredondados generosos.

---

## 2. Logo

Dois arquivos, ambos nesta mesma pasta:

| Arquivo | Quando usar |
|---|---|
| `ivc-logo-full.png` | Wordmark completo "Investidores.vc". Para a maioria das thumbnails (rodapé, canto, ou centralizado). |
| `ivc-logo-mark.png` | Símbolo `.vc` (anel amarelo + ponto). Quando o espaço é apertado ou o foco é o conteúdo. |

**Regras de uso:**
- **Margem mínima** ao redor do logo = altura da letra "i" do wordmark (≈ 1× o x-height).
- **Tamanho mínimo:** wordmark com altura ≥ 28px; mark com altura ≥ 24px.
- **Não:** distorcer, colorir, adicionar sombra/outline, rotacionar, sobrepor a fundos com baixo contraste.
- **Sobre fundo escuro** (`#1A1B1F`): use o `ivc-logo-full.png` como está (wordmark branco, ponto amarelo).
- **Sobre fundo claro/amarelo:** use uma versão em ink-900. Se não tiver, prefira o mark.

---

## 3. Cores

### Paleta principal (use estas 3 em quase tudo)

| Token | Hex | Papel |
|---|---|---|
| **Yellow 500** | `#FFBA00` | Cor da marca. CTAs, destaques, números importantes, fundo de "punch". |
| **Ink 900** | `#1A1B1F` | Fundo escuro, texto sobre claro, headlines de impacto. |
| **White** | `#FFFFFF` | Superfícies, texto sobre escuro/amarelo. |

### Suporte (texto e neutros)

| Token | Hex | Uso |
|---|---|---|
| Ink 700 | `#323232` | Texto principal sobre claro. |
| Ink 600 | `#4F4F4F` | Texto secundário / corpo. |
| Ink 400 | `#9194A6` | Captions, legendas, metadados. |
| Bg | `#F8F8F8` | Fundo neutro claro alternativo ao branco. |
| Yellow 50 | `#FFF9E9` | Fundo creme suave (variação quente do branco). |

### Semânticas (use só quando o conteúdo pedir)

| Token | Hex | Significado |
|---|---|---|
| Success | `#16A34A` | positivo, alta, lucro |
| Warning | `#F59E0B` | atenção, em curso |
| Danger | `#EF4444` | negativo, queda, perda |
| Info | `#2563EB` | informativo, neutro-frio |

### Pares aprovados para fundo + texto

- ✅ Amarelo `#FFBA00` + Ink 900 `#1A1B1F` → o par-assinatura. Use sem medo.
- ✅ Ink 900 `#1A1B1F` + Branco `#FFFFFF` → headlines fortes.
- ✅ Ink 900 `#1A1B1F` + Amarelo `#FFBA00` → palavras-âncora dentro de headline.
- ✅ Branco + Ink 700 `#323232` → corpo de texto.
- ❌ Amarelo + Branco → contraste insuficiente, evitar.
- ❌ Ink 400 + Branco → contraste fraco para texto.

---

## 4. Tipografia

**Família:** **Cera Pro** (geométrica sans-serif).
**Fallback:** `-apple-system, "SF Pro Display", "Segoe UI", Roboto, sans-serif`

### Hierarquia para thumbnails (1080×1080 ou 1080×1350)

| Papel | Peso | Tamanho sugerido | Tracking | Uso |
|---|---|---|---|---|
| **Headline** | Bold (700) | 84–120px | -0.02em | Frase principal da thumbnail |
| **Subhead** | Medium (500) | 40–56px | -0.01em | Apoio à headline |
| **Eyebrow / Label** | Bold (700) | 22–28px | +0.06em | UPPERCASE, acima da headline |
| **Body / Caption** | Regular (400) | 28–36px | 0 | Crédito, fonte, data |
| **Wordmark logo** | (logo file) | altura ~48–64px | — | Canto inferior |

### Regras
- **Sempre Cera Pro.** Se não tiver disponível, usar `-apple-system` / `SF Pro` antes de qualquer outra fonte.
- **Tracking apertado** (`-0.02em`) em headlines grandes. Tracking neutro em body.
- **Line-height** 1.05–1.15 em headlines, 1.4 em body.
- **Itálico:** só para nomes próprios ou ênfase pontual. Nunca para uma frase inteira.
- **CAIXA ALTA:** só em eyebrows/labels pequenas, com tracking +0.06em.

---

## 5. Espaçamentos

Sistema baseado em múltiplos de 4px. Para thumbnails 1080×1080, multiplique mentalmente por ~4 para escalar.

| Token | px | Uso |
|---|---|---|
| `space-1` | 4 | hairline interno |
| `space-2` | 8 | gap entre ícone e label |
| `space-3` | 12 | gap entre chips |
| `space-4` | 16 | gap entre elementos relacionados |
| `space-5` | 20 | padding interno padrão de card |
| `space-6` | 24 | margem externa de card |
| `space-8` | 32 | separação entre blocos |
| `space-12` | 48 | respiro de seção |
| `space-16` | 64 | respiro grande / hero |

### Margens de segurança (thumbnail Instagram)
- **Margem externa:** mínimo **64px** (em 1080×1080) de qualquer borda. Idealmente **96–120px**.
- **Logo no canto:** offset de 64–96px da borda mais próxima.
- **Headline:** sempre dentro do retângulo de safe-area (largura ≤ 80% do canvas).

---

## 6. Arredondamentos (radii)

| Token | px | Quando usar |
|---|---|---|
| `radius-sm` | 8 | chips pequenos, badges |
| `radius-md` | 12 | inputs, tags |
| `radius-lg` | 16 | cards padrão |
| `radius-xl` | 20 | cards de destaque (sector card) |
| `radius-2xl` | 24 | cards hero / placas grandes em thumbnails |
| `radius-pill` | 999 (totalmente arredondado) | botões CTA, chips, badges, bubbles |

**Regra geral:** quando em dúvida, use `radius-lg` (16px) para cards e `radius-pill` para botões. **Cantos quadrados (0px) só em fotografia full-bleed.**

Para thumbnails grandes, escale os radii ~3–4×: ex. um `radius-2xl` (24px) vira ~72–96px num canvas 1080.

---

## 7. Sombras

Sombras **suaves, frias, nunca coloridas.**

| Token | Valor | Uso |
|---|---|---|
| `shadow-sm` | `0 1px 3px rgba(0,0,0,0.08)` | placas leves |
| `shadow-md` | `0 2px 8px rgba(0,0,0,0.10)` | cards |
| `shadow-lg` | `0 8px 20px rgba(43,45,51,0.16)` | hero / floats — **sombra-assinatura** |

Para thumbnails, escale para `0 16px 40px rgba(0,0,0,0.18)` em elementos flutuantes.

---

## 8. Princípios para thumbnails Instagram

Em ordem de prioridade:

1. **Uma headline. Uma ideia. Um destaque.** Nunca empilhe 3 mensagens.
2. **Amarelo é o personagem principal.** Use como fundo, como sublinhado de palavra-chave, ou como pílula. Não trate como detalhe.
3. **Headlines em Cera Pro Bold, gigantes.** O texto precisa ser lido a 1cm de distância no Reels.
4. **Logo discreto, mas presente.** Sempre canto inferior (esquerda ou direita), nunca centralizado, nunca enorme.
5. **Sem gradientes coloridos.** Fundo sólido (preto, branco, amarelo, ou creme). Gradientes só do nosso conjunto premium (fintech, agritech, etc.) quando o tema pedir.
6. **Sem emojis.** Sem ícones decorativos. Sem confete. Sem brilho. A marca é calma.
7. **Hierarquia clara:** eyebrow pequeno em cima → headline gigante → subhead opcional → logo no canto. Nessa ordem visual.
8. **Cantos arredondados generosos** em qualquer placa interna (não use cantos quadrados em cards).

---

## 9. Layouts canônicos (3 que sempre funcionam)

### A · Pílula amarela
- Fundo: Ink 900 (`#1A1B1F`)
- Headline branca centralizada
- Palavra-chave dentro de uma **pílula amarela** (`#FFBA00`, radius 999, padding generoso, texto Ink 900)
- Logo branco no canto inferior

### B · Bloco amarelo
- Canvas dividido: 70% amarelo `#FFBA00` à esquerda + 30% Ink 900 à direita
- Headline em Ink 900 sobre o amarelo
- Logo wordmark no bloco preto

### C · Editorial
- Fundo branco ou creme `#FFF9E9`
- Eyebrow em CAIXA ALTA tracking aberto, cor Ink 600
- Headline gigante em Ink 900 (com 1 palavra em amarelo se quiser ênfase)
- Logo discreto canto inferior

---

## 10. Checklist de validação

Antes de publicar uma thumbnail, confira:

- [ ] Usa **apenas** Cera Pro (ou fallback iOS)
- [ ] Headline tem ≥ 84px e contraste AAA com o fundo
- [ ] Amarelo aparece em pelo menos 1 elemento estrutural (não só detalhe)
- [ ] Logo presente, no canto, não distorcido
- [ ] Margem ≥ 64px em todas as bordas
- [ ] Radii arredondados em qualquer placa interna
- [ ] Sem emoji, sem gradiente colorido fora da paleta, sem ícone decorativo
- [ ] Uma única ideia / mensagem central
