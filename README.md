# YT2MP3

YouTube-Link einfügen, Tonspur als MP3 (128/192/320 kbit/s) oder im Originalformat speichern.
Next.js-App für Vercel.

## So funktioniert's

1. `GET /api/info?url=…` liest Titel, Kanal, Länge und die verfügbaren Audiospuren über
   [youtubei.js](https://github.com/LuanRT/YouTube.js).
2. Der Browser lädt die Audiospur über `GET /api/chunk?v=…&itag=…&start=…` in Stücken von 4 MB
   (Vercel begrenzt Funktionsantworten auf 4,5 MB). Der Server holt nur Stream-Adressen, die er
   selbst ermittelt hat, ist also kein offener Proxy.
3. Der Browser dekodiert die Audiospur (Web Audio API) und kodiert sie in einem Web Worker mit
   [lamejs](https://github.com/breezystack/lamejs) zu MP3, inklusive ID3-Tags (Titel, Interpret,
   Cover).

MP3 gibt es für Videos bis 30 Minuten; längere (bis 3 Stunden) im Originalformat (M4A/WebM),
weil das Dekodieren sonst zu viel Arbeitsspeicher im Browser braucht.

## Entwicklung

```bash
npm install
npm run dev        # http://localhost:3000
npm run typecheck
npm run build
```

## Bekannte Einschränkung

YouTube blockiert Anfragen von Rechenzentrums-IPs (auch von Vercel) immer wieder mit
„Sign in to confirm you're not a bot“. Dann liefert `/api/info` eine entsprechende
Fehlermeldung. Lokal (Heim-IP) tritt das selten auf.

## Rechtliches

Nur Inhalte herunterladen, an denen du die Rechte hast oder die frei lizenziert sind, und die
Nutzungsbedingungen von YouTube beachten.
