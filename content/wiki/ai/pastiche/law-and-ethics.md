---
title: "Law and Ethics"
weight: 60
---

Copyright protects expression and not ideas, and style has always been filed on the idea side. That is the settled part, it long predates generative models, and it is also routinely overstated: courts treat stylistic similarity as evidence bearing on whether protected expression was copied, so "style is not copyrightable" is the beginning of the analysis rather than the end of it. The live questions are elsewhere — in the right of publicity, in what training on a corpus requires, and in a market-harm argument that has been formulated but not yet tested.

This page states what is decided and what is not. It is not legal advice.

## What is settled: style is not the protected thing

The rule comes out of the idea/expression dichotomy codified at 17 U.S.C. § 102(b). *Dave Grossman Designs v. Bortin* put it directly in 1972: an artist may use the same subject and style as another "so long as the second artist does not substantially copy [the first artist's] specific expression of his idea."

So writing new prose in the manner of a living novelist infringes nothing by itself. Neither does asking a model to. The novelist has copyright in their sentences, not in their sentence-making.

In *Steinberg v. Columbia Pictures* the court found a film poster infringed Saul Steinberg's *New Yorker* cover, and reasoned in part from style: "one can see the striking stylistic relationship between the posters, and since style is one ingredient of 'expression,' this relationship is significant."

Style is not independently protectable *and* stylistic similarity is admissible toward the finding that protectable expression was taken. Both hold at once. A pastiche that stays clear of the author's actual sentences is safe; a pastiche whose stylistic fidelity comes from reproducing particular passages is not made safe by the label.

## Pastiche is a defined legal category — outside the United States

The word this section is named after is a term of art in UK and EU copyright, which is not true of *style imitation*.

**United Kingdom.** Section 30A of the Copyright, Designs and Patents Act (CDPA), in force since 1 October 2014, makes fair dealing "for the purposes of caricature, parody or pastiche" a permitted act. The statute defines none of the three. The Intellectual Property Office's guidance fills the gap, and its gloss is close to this section's subject: pastiche is a composition "made up of selections from various sources or one that imitates the style of another artist or period."

**European Union.** Article 17(7) of the 2019 Digital Single Market (DSM) directive makes the caricature, parody and pastiche exception mandatory, so member states cannot decline to have one — but only for uses on online content-sharing platforms. These are autonomous concepts of EU law, to be interpreted uniformly across member states; following the Court of Justice of the European Union (CJEU) approach to parody, their meaning is their ordinary meaning in everyday language.

**United States.** There is no pastiche exception. There is fair use, and its four factors, applied case by case. A US analysis of the same act runs through transformativeness and market effect rather than through a named category.

The practical consequence is that the same output can be a recognized statutory category in one jurisdiction and an open four-factor question in another, on facts that have not changed.

## What is live

**Training.** In *Bartz v. Anthropic*, Judge Alsup held in June 2025 that training on lawfully acquired books was "quintessentially transformative" and fair use, while downloading and retaining pirated copies was not. The case settled for a minimum of $1.5 billion — roughly $3,000 per work — with final judgment entered on 20 July 2026. The holding is about acquisition, not about style: it says nothing about whether output resembling an author is a problem.

**Output.** *Andersen v. Stability AI* is the case that reaches the question. The artists' Digital Millennium Copyright Act §1202 claims were dismissed with prejudice in August 2024; direct infringement claims are proceeding to a jury trial scheduled to open on 8 September 2026, the first in the United States over AI training. The trial had not opened when this page was written. It is the first proceeding likely to produce a reference point for style-mimicry claims specifically.

**Market dilution.** The US Copyright Office's Part 3 report on generative training, released in prepublication form on 9 May 2025, introduced dilution as a fourth-factor harm: AI output can damage the market for human work by saturating it, without any individual output being infringing. The report analyses training rather than declaring style protectable, and this is where the strongest argument for regulating imitation currently sits — an economic harm the existing doctrine does not measure, since factor four asks about substitution for *the work*, and the harm alleged is substitution for *the author*.

**The counter-argument is not weak.** Extending copyright to style would break the idea/expression line that the whole system rests on, and would make the ordinary business of literature — influence, homage, school, movement — actionable. Every writer learns by imitation. A right in style is a right against being learned from.

## The closer legal hook is identity, not expression

Where imitation has actually been successfully sued in the US, it was not under copyright.

*Midler v. Ford Motor Co.* (9th Cir. 1988) held that deliberately imitating Bette Midler's distinctive voice in an advertisement, after she declined to license it, violated her common-law right of publicity. *Waits v. Frito-Lay* (9th Cir. 1992) affirmed the doctrine on the same facts with Tom Waits. In neither case did the defendant copy a recording; they hired someone to sound like the plaintiff. Copyright had nothing to say and the right of publicity did.

That is the doctrine shaped like the problem: it protects a persona rather than a work, it triggers on commercial use, and it does not require that anything expressive be taken. It is also state law, patchwork, and mostly litigated over voice and likeness rather than prose.

Two developments extend it toward generated media:

- **Tennessee's ELVIS Act**, effective 1 July 2024, was the first US state law to explicitly cover AI-generated voice replicas.
- **The NO FAKES Act** would create a federal digital-replica right in voice and visual likeness. Reintroduced in April 2025, it was advanced unanimously by the Senate Judiciary Committee on 18 June 2026 and remains pending. It would not preempt state statutes in existence as of 2 January 2025, so the ELVIS Act would survive it.

Note what these cover and what they do not. Voice and likeness, not prose style. A writer's manner is not a digital replica of them, and no enacted statute currently treats it as one.

## Where the public domain sits

Less centrally than intuition suggests, because the public domain governs *copying the text*, and style was never covered in the first place.

[Mikros's stylometric study](/wiki/ai/pastiche/what-transfers) makes the point by accident: it imitated Mary Shelley from *Frankenstein* (1818), which is public domain worldwide, and Ernest Hemingway from *The Old Man and the Sea* (1952), which is under US copyright until 2048. Under copyright law the two imitations stand identically, because neither reproduces protected expression. Hemingway's *The Sun Also Rises* (1926) entered the US public domain on 1 January 2022, and that changed what may be reprinted, not what may be imitated.

Where the public domain does bite is on the inputs. Quoting the author at length in a prompt, storing a corpus, or distributing the excerpts are reproduction questions, and those turn on term. It is the [in-context learning](/wiki/ai/pastiche/rules-versus-examples) route to a better pastiche that has a copyright surface, not the pastiche.

Publicity rights do not track copyright term. They are state law, and postmortem duration varies by state rather than expiring on a single federal schedule, so a long-dead author's estate may hold rights in the persona even where every work is free.

## The ethical question the law does not reach

Most of what people object to is not infringement, and saying so is not a defence.

**Deception is the line that matters and it is not a copyright line.** [The three tasks](/wiki/ai/pastiche) separate here: pastiche presented as pastiche is a genre with a long history; the same text presented as the author's is forgery, and the wrong is the claim rather than the prose. Fraud, defamation and passing-off already reach it. The technical finding that [imitations remain identifiable](/wiki/ai/pastiche/authorship-survives) is a fact about detection, not a reason the attempt was acceptable.

**Consent to being simulated.** Nudo et al. [built agents from 1,186 identifiable people](/wiki/ai/pastiche/generative-exaggeration#more-information-worse-portrait) using their public posts, and produced output more toxic and more partisan than those people were. Nothing there is a copyright question, everything published was public, and the result still misrepresents named individuals. Public availability is not consent to be extrapolated.

**Attribution in ordinary use.** Most applied pastiche is unglamorous — matching a documentation set, a publication's voice, a colleague's register. The relevant norm is disclosure to whoever will act on the text, and it is closer to editorial practice than to law.

## Related

- [Pastiche](/wiki/ai/pastiche) — the distinction between imitation, transfer and forgery that this page's analysis rests on.
- [Authorship survives imitation](/wiki/ai/pastiche/authorship-survives) — what is technically detectable, which is a separate question from what is permitted.
- [Generative exaggeration](/wiki/ai/pastiche/generative-exaggeration) — the simulation study behind the consent question, and what it did to the people it modelled.
- [Rules versus examples](/wiki/ai/pastiche/rules-versus-examples) — the in-context route that does have a reproduction surface.

## Further reading

- Ginsburg, [AI Image Outputs "in the style of ..."](https://scholarship.law.columbia.edu/faculty_scholarship/4544), Columbia Law School faculty scholarship (2024)
- US Copyright Office, [Copyright and Artificial Intelligence, Part 3: Generative AI Training](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-Pre-Publication-Version.pdf) (prepublication, May 2025)
- US Copyright Office, [Copyright and Artificial Intelligence, Part 2: Copyrightability](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf) (January 2025)
- [Copyright, Designs and Patents Act 1988, Section 30A](https://www.legislation.gov.uk/ukpga/1988/48/section/30A)
- [Directive (EU) 2019/790 on copyright in the Digital Single Market, Article 17](https://eur-lex.europa.eu/eli/dir/2019/790/oj)
- [Steinberg v. Columbia Pictures Industries, Inc., 663 F. Supp. 706 (S.D.N.Y. 1987)](https://law.justia.com/cases/federal/district-courts/FSupp/663/706/1414117/)
- Congressional Research Service, [Generative Artificial Intelligence and Copyright Law](https://www.congress.gov/crs-product/LSB10922)
