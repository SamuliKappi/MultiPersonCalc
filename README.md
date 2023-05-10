### General Description
The concept behind our application is a multiplayer calculator, where both you and other people, anonymous to you, may attempt to perform or sabotage the act of completing basic mathematical calculations.

### Structure of the Program
The program effectively consists of two larger areas: the application which the user uses, as well as the Flask server used to perform the background logic and validate the user's credentials as well as their input.

### Secure programming solutions

#### SANS 25

**1. Out-of-bounds Write:** Out-of-bounds write errors are not applicable to Python 3.X.
**2. Cross-site Scripting:** Application does not allow for free-form user input.
**3. SQL Injection:** Application does not utilize SQL databases.
**4. Improper Input Validation:** User input is limited, and is always validated server-side.
**5. Out-of-bounds Read:** Out-of-bounds write errors are not applicable to Python 3.X.
**6. OS Command Injection:** Application does not use string_exec, which is the only applicable case for OS commands to be misinterpreted.
**7. Use After Free:** Use after free errors are not applicable to Python 3.X.
**8. Improper Limitation of a Pathname to a Restricted Directory:** Application uses hard-coded pathnames.
**9. Cross-Site Request Forgery:** Attacker must possess valid credentials or a cookie.
**10. 	
Unrestricted Upload of File with Dangerous Type:** Application does not support upload of any type of file.
**11. NULL Pointer Dereference:** NULL pointer dereference errors are not applicable to Python 3.X.
**12. Deserialization of Untrusted Data:** All input is validated server-side.
**13. Integer Overflow or Wraparound:** Integer overflow or wraparound errors are not applicable to Python 3.X.
**14. Improper Authentication:** User tokens and login credentials are always validated.
**15. Use of Hard-coded Credentials:** All credentials are user-made or automatically randomized.
**16. Missing Authorization:** The server requires authorization for every end-point except for signup and login.
**17. Command Injection:** Application does not create commands using externally-influenced input.
**18. Missing Authentication for Critical Function:** The server requires authorization for every end-point except for signup and login.
**19. Improper Restriction of Operations within the Bounds of a Memory Buffer:** These types of errors are not applicable to Python 3.X.
**20. Incorrect Default Permissions:** User has no default permissions.
**21. Server-Side Request Forgery:** The server accepts urls as part of a password, but treats them as strings.
**22. Race Condition:** Application nor server uses concurrency.
**23. Uncontrolled Resource Consumption:** Technically possible, although due to only having one thread, the server will only consume a limited amount of resources.
**24. Improper Restriction of XML External Entity Reference:** Application does not utilize XML.
**25. Code Injection:** The server accepts code segments as part of a password, but treats them as strings.

### Testing

Testing was done manually, both through application testing, static code analysis and by prompting the server with various types of erroneous requests.

### Missing Implementations

### Known Security Issues or Vulnerabilities
The server is currently comparatively prone to multi-directional DDoS attacks which overload the server, as requests are not denied, and a single thread may prove to not be able to support the mass of requests sent to it.

### Improvement Suggestions
The system would be a more functional unit if a Publish / Subscribe pattern was implemented, as this would allow for a non-manual refreshing pattern to work.