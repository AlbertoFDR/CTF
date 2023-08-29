## ProjectSekai -- Frog-WAF (29 Solves)
### Not solved during CTF

The key thing of this challenge is the following vulnerability `Therefore if an attacker can inject arbitrary data in the error message template being passed to ConstraintValidatorContext.buildConstraintViolationWithTemplate() argument, they will be able to run arbitrary Java code.` ([link](https://securitylab.github.com/advisories/GHSL-2020-204-cwa-ssti/)). For reaching this part we need to create a new contact inserting our payload in the country to reach the following code of file `CountryValidator.java`: 

```java
if (!isValid) {
     val message = String.format("%s is not a valid country", input);
     constraintContext.disableDefaultConstraintViolation();
     constraintContext.buildConstraintViolationWithTemplate(message)
             .addConstraintViolation();
}
```

In this moment, you need to take care of the valid characters for creating a valid payload (check `AttackTypes.java`). In order to build our payload we will use `[]` and `getSize()` function and other method names to construct our final payload without using their protections. For the final script check `solve.py`. Flag: `Flag: SEKAI{0h_w0w_y0u_r34lly_b34t_fr0g_wAf_c0ngr4ts!!!!}`.
