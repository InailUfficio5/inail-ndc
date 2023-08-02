# Asset per il catalogo nazionale della semantica dei dati
Questo è il repository INAIL per l'alimentazione del National Data Catalog (NDC): https://www.schema.gov.it/.
Esso contiene l'ontologia di INAIL che descrive il patrimonio informativo dell'ente relativamente al dominio di _malattie professionali_ ed  _infortuni_.

Il catalogo nazionale della semantica dei dati, o NDC, consente:
> "Ricerca e riuso di asset semantici, tra cui ontologie, schemi dati e vocabolari controllati per supportare lo sviluppo di API semanticamente e sintatticamente interoperabili"

## Organizzazione delle informazioni

I file presenti in questo repository sono organizzati secondo la seguente alberatura:

```bash
┌─ assets/ontologies/
│  ├─ mp-inf/
│  │  └─ {version}/MP_INF.ttl
│  └─ notes.md
├─ assets/controlled-vocabularies/
│  └─ ...
├─ assets/schemas/
│  ├─ esito-definizione
│  │  └─ esito-definizione.oas3.yaml
│  ├─ inabilita-temporanea
│  │  └─ inabilita-temporanea.oas3.yaml
│  ├─ indennizzo
│  │  └─ indennizzo.oas3.yaml
│  ├─ infortunato
│  │  └─ infortunato.oas3.yaml
│  ├─ infortunio
│  │  └─ infortunio.oas3.yaml
│  ├─ malattia-professionale
│  │  └─ malattia-profesisonale.oas3.yaml
│  ├─ prestazione-economica
│  │  └─ prestazione-economica.oas3.yaml
│  ├─ riapertura-trattazione
│  │  └─ riapertura-trattazione.oas3.yaml
│  ├─ tecnopatico
│  │  └─ tecnopatico.oas3.yaml
│  ├─ tipo-indennizzo
│  │  └─ tipo-indennizzo.oas3.yaml
│  ├─ tipo-trattazione
│  │  └─ tipo-trattazione.oas3.yaml
│  └─ trattazione
│     └─ trattazione.oas3.yaml
├─ README.md
└─ publiccode.yaml
```

Ontologie e [vocabolari controllati](https://www.agid.gov.it/it/dati/vocabolari-controllati) sono documenti [RDF](https://www.w3.org/RDF/) serializzati in formato [TURTLE](https://www.w3.org/TR/turtle/) mentre gli schemi  [Open Api 3 (OAS3)](https://spec.openapis.org/oas/v3.1.0) sono serializzati in formato [YAML](https://yaml.org/).

## Licenza
Tutti i moduli ontologici sono rilasciati sotto la licenza aperta Creative Commons Attribution 4.0
