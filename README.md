# Loggning och felsökning

## Introduktion

Detta är en praktisk övning som syftar till att utforska loggning och felsökning. Genom att följa stegen nedan kommer du att:

- Skapa två AWS Lambda-funktioner (ett REST API samt en webb-app) genom OpenTofu.
- Interagera med webbapplikationen för att identifiera och analysera fel.
- Utvärdera, reflektera och förbättra loggning för att underlätta felsökning.

## Förberedelser

1. **Klona repo och navigera till projektmappen:**
   ```bash
   git clone https://github.com/khdev-devops/infra-mar20-logging.git
   cd infra-mar20-logging
   ```

2. **Installera OpenTofu i AWS CloudShell:**
   ```bash
   ./tofu_install_and_init.sh
   ```

3. **Initiera och applicera OpenTofu-konfigurationen:**
   ```bash
   # tofu init gjordes av scriptet i förra steget
   tofu plan
   tofu apply
   ```

## Utforska webbapplikationen och analysera loggar

Efter att infrastrukturen har skapats, följ dessa steg:

1. **Åtkomst till webbapplikationen:**
   - Hämta URL:en för webbapplikationen från utdata efter `tofu apply`.
   - Öppna URL:en i din webbläsare.

2. **Interagera med applikationen:**
   - Uppdatera sidan flera gånger för att generera olika förfrågningar.

3. **Identifiera och analysera fel:**
   - Om ett fel inträffar, notera meddelandet som visas i webbläsaren.
   - Öppna AWS Management Console och navigera till CloudWatch för att visa loggarna för Lambda-funktionerna.
   - Analysera loggarna för att förstå orsaken till felet.

4. **Utvärdera och förbättra loggningspraxis:**
   - Granska källkoden för att se hur loggningen är implementerad.
   - Fundera över hur loggningen kan förbättras för att underlätta felsökning.

## Rensa upp resurser

När du är klar med övningen, se till att ta bort de resurser som skapats för att undvika onödiga kostnader:

1. **Ta bort resurserna med OpenTofu:**
   ```bash
   tofu destroy
   ```
