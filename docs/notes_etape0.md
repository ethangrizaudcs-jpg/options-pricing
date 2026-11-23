# Étape 0 : introduction à la finance de marché

> Notes de cours personnelles. Objectif : poser le vocabulaire et la logique de desk avant d'attaquer Black-Scholes.

---

## 1. Les briques de base

### Action (*stock, equity, share*)
Une part de propriété d'une entreprise. Son prix **S_t** (le **spot**) est fixé en continu par l'offre et la demande sur un marché organisé (Euronext Paris, NYSE…).
- **Bid** : meilleur prix auquel quelqu'un veut acheter. **Ask / offer** : meilleur prix auquel quelqu'un veut vendre. **Mid** = (bid + ask)/2. **Spread** = ask − bid (ce que coûte un aller-retour, en gros).
- Être **long** = détenir (on gagne si le prix monte). Être **short** = avoir vendu sans détenir, via un emprunt de titres (on gagne si le prix baisse).

### Indice (*index*)
Un panier pondéré d'actions, calculé en continu : **CAC 40** (40 grandes capitalisations françaises), **Euro Stoxx 50** (SX5E, 50 de la zone euro, *le* sous-jacent roi des produits structurés européens), **S&P 500** (SPX, 500 américaines). On ne peut pas « acheter l'indice » directement, mais on peut acheter un **ETF** qui le réplique (SPY pour le S&P 500) ou un **future** dessus.

### Taux sans risque (*risk-free rate*, r)
Le taux auquel on peut prêter/emprunter « sans risque de défaut ». En pratique on prend un taux interbancaire ou overnight (**€STR** en euro, **SOFR** en dollar) ou le rendement d'un emprunt d'État court. Sert à **actualiser** : 1 € reçu dans T ans vaut aujourd'hui e^{−rT} € (en composition continue, la convention qu'on utilisera partout).
- **Zéro-coupon** (*zero-coupon bond*) : titre qui paie 1 à la date T et rien avant. Prix B(0,T) = e^{−rT}.

### Dividende (*dividend*, q)
Une part du bénéfice reversée aux actionnaires. Le jour du **détachement** (*ex-dividend date*), le cours baisse mécaniquement d'environ le montant du dividende (sinon arbitrage). On le modélise souvent par un **rendement continu q** (*dividend yield*). Conséquence clé : le **forward** (prix convenu aujourd'hui pour une livraison en T) vaut

$$F_0 = S_0 \, e^{(r-q)T}.$$

*Preuve par réplication* : emprunter S_0 e^{−qT} au taux r, acheter e^{−qT} action, réinvestir les dividendes en actions → on détient exactement 1 action en T et on doit rembourser S_0 e^{(r−q)T}. Tout autre prix forward permet un arbitrage.

---

## 2. Les options

### Définitions
Une option est un **contrat** qui donne à l'acheteur le **droit, mais pas l'obligation**, d'acheter ou de vendre un sous-jacent à un prix fixé à l'avance.

| | Call (option d'achat) | Put (option de vente) |
|---|---|---|
| Droit de… | acheter à K | vendre à K |
| Payoff à maturité | (S_T − K)⁺ | (K − S_T)⁺ |
| Gagne quand… | le sous-jacent monte | le sous-jacent baisse |

- **K** : prix d'exercice (*strike*). **T** : maturité / échéance (*maturity, expiry*).
- **Prime** (*premium*) : le prix payé aujourd'hui par l'acheteur au vendeur. C'est ce qu'on cherche à calculer dans tout le projet.
- **Européenne** : exerçable seulement en T. **Américaine** : exerçable à tout instant t ≤ T (→ problème de temps d'arrêt optimal ; un call américain sur action sans dividende n'est jamais exercé avant T, donc vaut le call européen).
- **Payoff** ≠ **P&L** : le payoff est le flux reçu à maturité ; le P&L (*profit and loss*) de l'acheteur = payoff − prime capitalisée.

### Moneyness
Pour un call : **dans la monnaie** (*in-the-money, ITM*) si S > K ; **à la monnaie** (*at-the-money, ATM*) si S ≈ K ; **hors de la monnaie** (*out-of-the-money, OTM*) si S < K. C'est l'inverse pour un put. On parle aussi de strike en % du spot (« le put 90 % » = strike à 90 % du spot).
- **Valeur intrinsèque** : (S − K)⁺ pour un call. **Valeur temps** (*time value*) = prime − valeur intrinsèque ≥ 0 : la valeur de l'optionalité restante, qui dépend surtout de la volatilité.

### Exemple chiffré
Action à S_0 = 100 €. Call 1 an strike 100, prime 9,41 €.
- S_T = 130 → payoff 30, P&L acheteur ≈ 30 − 9,41 = **+20,59** (pour 9,41 investis : +219 %, alors qu'acheter l'action rapporte +30 %). C'est l'**effet de levier**.
- S_T = 90 → payoff 0, P&L = **−9,41** : la perte est bornée par la prime.
- Le vendeur a exactement le P&L opposé : il encaisse la prime mais a une perte **potentiellement illimitée** sur un call. D'où le besoin de **couverture** (étape 2).

### Pourquoi achète-t-on des options ?
1. **Couverture** (*hedging*) : un gérant détient 10 M€ d'actions Euro Stoxx 50 et a peur d'un krach. Il achète des **puts 90 %** : en dessous de −10 %, chaque euro perdu sur les actions est compensé par le put. C'est une **assurance**, la prime en est le coût. Cette demande structurelle de protection explique pourquoi les puts OTM sont « chers » (le **skew**, étape 3).
2. **Spéculation / prise de vue** : levier sur une direction (call si haussier), ou pari sur la **volatilité** elle-même (acheter call + put ATM = **straddle**, gagne si ça bouge fort, peu importe le sens).
3. **Rendement** : vendre des options pour encaisser la prime (*covered call* : on détient l'action et on vend un call OTM). C'est exactement ce que fait, sans le savoir, l'acheteur d'un autocall (étape 4) : il **vend de la vol**.

### Marchés listés vs OTC
- **Listés** (*listed, exchange-traded*) : contrats standardisés (strikes, maturités fixes) sur Eurex, CBOE… avec chambre de compensation.
- **De gré à gré** (*OTC, over-the-counter*) : contrat bilatéral sur mesure entre une banque et un client. Tous les produits structurés sont OTC.

---

## 3. La salle de marché (*trading floor*)

Organisation par **desks** (Equity Derivatives, Rates, FX, Credit, Commodities). Sur un desk dérivés actions, le front office comprend :

| Métier | Rôle | Une journée type |
|---|---|---|
| **Sales** | Relation client (gérants, assureurs, banques privées, hedge funds). Comprend le besoin, transmet les demandes de prix (*RFQ, request for quote*), vend les idées. | Point marché du matin envoyé aux clients, appels, envoi d'idées (« le skew est cher, voici un produit qui en profite »), négociation du prix avec le trader. |
| **Trader** | Gère un **book** (portefeuille de positions) et son risque. Donne les prix (*market making* : cote un bid et un ask), puis **couvre** le risque. Responsable du P&L quotidien. | Avant l'ouverture : revue des risques (greeks du book) et du P&L de la veille (*P&L explain*). Journée : cote les RFQ, ajuste la couverture delta, gère gamma/vega, suit les événements (résultats, dividendes, banques centrales). Soir : explique son P&L. |
| **Structureur** | Conçoit des **produits structurés** sur mesure en assemblant des briques (zéro-coupon + options). Trouve le coupon qui répond au besoin du client tout en dégageant une marge. | Construit des *term sheets*, calcule les coupons équitables, fait des propositions de produits adaptées au marché (« avec la vol actuelle, on peut offrir 8 % par an sur un autocall barrière 60 % »). |
| **Quant** | Développe et maintient les **modèles** de pricing et de risque (vol locale, vol stochastique, Monte Carlo, calibration). *Desk quant* : collé au trading, outils rapides. *Model validation* : vérifie les modèles en indépendance (risk). | Code (C++/Python), calibration, résolution de problèmes de pricing remontés par les traders. |

Autour : **middle office / risk** (contrôle des limites, VaR, validation du P&L), **back office** (règlement-livraison, confirmations).

**Comment ils interagissent, sur un exemple** : un assureur veut un placement sur 5 ans indexé à l'Euro Stoxx 50 avec protection partielle du capital. Le **sales** remonte le besoin ; le **structureur** propose un autocall et calcule le coupon ; le **trader** exotique donne le prix des options embarquées et, une fois le produit vendu, porte et couvre le risque pendant 5 ans ; le **quant** a fourni le modèle qui price le produit.

---

## 4. Absence d'opportunité d'arbitrage (AOA) et parité call-put

### Arbitrage (*arbitrage*)
Une stratégie qui **ne coûte rien** aujourd'hui, **ne peut jamais perdre**, et **gagne avec probabilité > 0**. Formellement, un portefeuille autofinancé de valeur V avec V_0 = 0, V_T ≥ 0 p.s. et P(V_T > 0) > 0. L'**AOA** suppose que de telles stratégies n'existent pas (s'il en apparaît, les arbitragistes les exploitent et les prix se réalignent).

Conséquence fondamentale (**loi du prix unique**) : deux portefeuilles qui ont le même flux en T ont le même prix aujourd'hui. C'est *le* raisonnement de base de tout pricing : **le prix d'un produit = le coût de sa réplication**. (Résultat profond, le **premier théorème fondamental** : AOA ⟺ existence d'une probabilité risque-neutre Q équivalente sous laquelle les prix actualisés sont des martingales. On y vient à l'étape 1.)

### Parité call-put (*put-call parity*)
Pour un call et un put européens de même strike K et même maturité T, sur une action de rendement de dividende q :

$$C_0 - P_0 = S_0 e^{-qT} - K e^{-rT}.$$

**Preuve.** Comparer en T :
- Portefeuille A : long call, short put → payoff (S_T − K)⁺ − (K − S_T)⁺ = **S_T − K** (identité x⁺ − (−x)⁺ = x).
- Portefeuille B : e^{−qT} action (dividendes réinvestis) et emprunt de K e^{−rT} → vaut **S_T − K** en T.

Même payoff dans tous les états du monde ⇒ même prix aujourd'hui par AOA. ∎

Remarques :
- **Aucune hypothèse de modèle** (pas de Black-Scholes, pas de loi de S_T) : c'est un résultat d'AOA pur. Il est donc vrai sur le marché réel (aux frictions près) et sert à tester la cohérence des données (étape 3).
- Long call + short put = **forward synthétique** : C − P = e^{−rT}(F_0 − K). Donc **à K = F_0** (strike « ATM forward »), call et put valent le même prix.
- Ne vaut que pour les **européennes**.

### Exemple chiffré d'arbitrage
S_0 = 100, K = 100, T = 1 an, r = 3 %, q = 0. Alors K e^{−rT} = 97,04 et la parité impose C − P = 2,96.
Le call cote 9,41. Le put devrait donc coter 6,46. Supposons qu'il cote **6,00** (put trop bon marché) :
- Aujourd'hui : acheter le put (−6,00), acheter l'action (−100), vendre le call (+9,41) → coût net 96,59, que j'emprunte. **Mise de fonds : 0.**
- En T : put + action − call vaut toujours exactement K = 100, quel que soit S_T. Je rembourse 96,59 × e^{0,03} = 99,53.
- **Gain certain : 0,47 €** par option. Les arbitragistes achètent le put jusqu'à ce que son prix remonte à 6,46.

### Bornes simples (AOA)
Pour un call européen sans dividende : (S_0 − K e^{−rT})⁺ ≤ C_0 ≤ S_0. Pour un put : (K e^{−rT} − S_0)⁺ ≤ P_0 ≤ K e^{−rT}. (On les approfondira à l'étape 3.)

---

## 5. Lexique de desk (FR / EN)

| Français | Anglais | Sens |
|---|---|---|
| sous-jacent | underlying | actif sur lequel porte l'option |
| cours, spot | spot | prix actuel du sous-jacent |
| prix d'exercice | strike | K |
| échéance, maturité | expiry, maturity | T |
| prime | premium | prix de l'option |
| à / dans / hors de la monnaie | ATM / ITM / OTM | position du spot par rapport au strike |
| acheteur / vendeur | long / short | « je suis long 100 calls » |
| couverture | hedge | position qui neutralise un risque |
| portefeuille de positions | book | l'ensemble des positions d'un trader |
| demande de prix | RFQ (request for quote) | un client demande un prix |
| fourchette | bid / ask (offer), spread | prix d'achat / de vente du market maker |
| nominal | notional | montant de référence du contrat |
| gré à gré | OTC | contrat bilatéral sur mesure |
| volatilité | vol | amplitude des variations, le paramètre-clé |
| P&L, résultat | P&L | profit and loss |

---

## 6. Questions d'entretien

**1. Quelle est la différence entre un call et un put ? Dessinez leurs payoffs.**
Call : droit d'acheter à K, payoff (S_T − K)⁺, en forme de crosse de hockey croissante. Put : droit de vendre à K, payoff (K − S_T)⁺, décroissante. Le vendeur a le payoff opposé (et a encaissé la prime).

**2. Quelle est la perte maximale de l'acheteur d'un call ? Du vendeur ?**
Acheteur : la prime. Vendeur d'un call : illimitée (S_T peut monter sans borne). Vendeur d'un put : K − prime (si S_T = 0).

**3. Énoncez et démontrez la parité call-put.**
C − P = S e^{−qT} − K e^{−rT}. Long call + short put paie S_T − K, comme un portefeuille action + emprunt de K e^{−rT}. Même payoff ⇒ même prix par AOA. Sans hypothèse de modèle.

**4. Un call et un put ATM de même maturité : lequel est le plus cher ?**
Piège classique. Si « ATM » = ATM spot (K = S) et r > q, le **call** est plus cher, car C − P = S(e^{−qT} − e^{−rT}) > 0. À K = forward, ils ont exactement le même prix.

**5. Le call vaut 10, le put 5, S = 100, K = 100, r = 0 (pas de dividende). Que faites-vous ?**
La parité impose C − P = 0 ; ici C − P = 5. Le call est trop cher relativement au put : vendre le call, acheter le put, acheter l'action. Flux initial : +10 − 5 − 100 = −95, financé par un emprunt de 95. En T, action + put − call vaut toujours K = 100 : je rembourse 95, gain certain de 5.

**6. Pourquoi un call américain sur une action sans dividende n'est-il jamais exercé avant l'échéance ?**
C ≥ S − K e^{−rT} > S − K pour r > 0 : l'option vaut plus vivante qu'exercée (on garde la valeur temps et on paie K plus tard). Mieux vaut la revendre. Avec dividendes, l'exercice anticipé juste avant le détachement peut être optimal.

**7. Pourquoi un investisseur achèterait-il un put ?**
Couverture (assurance d'un portefeuille actions contre une baisse) ou spéculation baissière à perte limitée. La demande structurelle de protection rend les puts OTM chers : c'est une des origines du skew.

**8. Qu'est-ce qu'un arbitrage ? Pourquoi suppose-t-on qu'il n'y en a pas ?**
Stratégie à coût nul, sans risque de perte, avec probabilité positive de gain. On suppose l'AOA car les arbitrages sont exploités et disparaissent vite ; c'est l'hypothèse qui permet de pricer par réplication.

**9. Quel est le prix forward d'une action ? Pourquoi n'est-ce pas l'espérance du prix futur ?**
F = S e^{(r−q)T}, obtenu par réplication (acheter l'action en empruntant). Il ne dépend pas des anticipations des agents : si le forward cotait autre chose, on arbitrerait avec l'action et le cash. Même idée que « μ disparaît du prix d'une option » (étape 1).

**10. Quelle est la différence entre un trader, un structureur et un sales ?**
Le sales gère la relation client et transmet les besoins ; le structureur conçoit le produit sur mesure et calcule ses conditions (coupon, barrières) ; le trader donne le prix, porte le risque dans son book et le couvre, et répond de son P&L.
