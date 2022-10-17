#!/usr/bin/env python
# coding: utf-8

# In[19]:


logs = [
    '{"green":["alliances.gobble.plodded","stringers.overthrows.trackable","piggybacking.psychics.zigzags","footnote.veneered.garish","sparsely.sieved.parameter","gingers.preschools.archly","professors.disloyal.interjects","hailstorm.alienates.inasmuch","detention.accuracies.decomposing","developmental.tidier.competitively","showstoppers.eyestrain.breakthroughs","bribery.warded.abrasion","unwind.cashier.accosted","unwind.cashier.accosted","caverns.birdman.moderators","slap.wavery.militant","joyriding.absentee.winemaking","yeasts.violin.shim","honeymooned.togas.unpopularity","mathematician.resurgent.nimbly","gigabytes.probable.snappers","boxes.guttered.disavows","rebounders.realm.aperture","mediums.songwriting.compensator","reveal.scuffles.probiotics","tinges.motorcycling.motivation","inoffensive.quilters.podiatry","vestiges.misplacing.virtuosity","rewire.daylights.soundless","inculcating.nozzles.whelk"],"orange":["hibiscus.slighter.difference","microprocessors.cannily.airframe","declarations.foretells.sergeant","alumni.anvils.searchingly","shiftless.administration.noisome","spicy.misjudges.dawning","turntables.academics.bartered","risers.teetering.weeknights","wealthier.exactly.unimpeded","persuasively.wildebeest.insinuate","twisty.disregard.violin","recency.bandmates.lacy"]}',
    "{\"green\":[\"cushioning.inhibition.abdicating\",\"playoff.giveth.nomadism\",\"frown.response.ratted\",\"determinist.anecdotal.fluctuating\",\"thickly.amorality.misfire\",\"antiquities.fatness.plaques\",\"succinct.cramps.discoverers\",\"dots.iniquity.waterskiing\",\"agave.mascot.multivitamins\",\"commissary.dubiously.imperative\",\"unprofessional.brisker.purloined\",\"canines.semicolon.plural\",\"lawn.concoct.disquieting\",\"anticompetitive.clandestinely.underfoot\",\"outstanding.overstepping.seaports\",\"wrecker.biogenic.plagiarist\",\"rearrangement.trills.remarked\",\"mainland.alumnus.attics\",\"lavishes.breadstick.renovating\",\"rats.intimidator.ginormous\",\"hipped.franchises.inadvisable\",\"sorcerer.precipice.yeast\",\"likeliest.unpaged.late\",\"renounce.perfect.recompose\",\"words.busywork.range\",\"guested.hypothermic.placating\",\"wretched.gauzy.doorknobs\",\"disposes.eying.teats\",\"foreseen.rehab.coextensive\",\"hardly.reinsurance.withstood\",\"posed.remake.shyness\",\"stringy.reassigning.orphanage\"],\"orange\":[\"fridays.forest.attendees\",\"commissary.miming.forfeits\",\"floods.fatherland.tickler\",\"content.outriggers.shaped\",\"decimal.senselessness.hooked\",\"swifter.nostalgic.municipal\",\"enervating.crashes.reference\",\"untraceable.cashed.privations\",\"architects.mackerels.uneconomical\",\"emancipation.encased.traipse\",\"playable.uplifted.homelike\",\"playable.uplifted.homelike\",\"agreeable.inventing.eldercare\",\"selectable.necessities.gush\",\"dependents.amplifier.summoned\",\"encouraged.chin.untested\"]}",
    '{"green":["washdown.returns.acupuncturist","overplaying.upbringings.snipped","overplaying.upbringings.snipped","untidily.washings.crabmeat","scissored.figs.kiosks","doorways.discard.manatee","lobbies.automates.broth","biology.coeducation.complainer"],"orange":["crane.melodramatic.carmaker","customer.roofing.antibacterial","customer.roofing.antibacterial","customer.roofing.antibacterial","videotape.conspiracy.modulation","dare.wrestlers.winemakers","metalworker.ruinously.recombined","sonnet.butterfly.manipulation","stoking.heartbreakers.soundbites"]}',
    "{\"green\":[\"viable.legislative.clambers\",\"sung.portrayed.booths\",\"riverbed.government.birdhouses\",\"particulars.sawdust.rind\",\"sigh.dangling.coda\",\"vexed.inspire.battles\",\"ratchet.meaningfulness.unbolt\"],\"orange\":[\"expendable.factoids.paparazzo\",\"unchanging.distort.trapped\",\"undersized.donates.believe\",\"quantities.traditional.fusses\",\"scallop.enamel.healer\",\"interloper.deletes.flora\",\"brining.gaffer.sinkholes\",\"flatters.casework.transactional\",\"thumbs.shimmery.hairpin\",\"contrivance.rounding.grating\",\"toughness.sham.crusting\",\"slumbered.zapped.miscalculated\",\"causeways.evolution.wallpapers\",\"divots.irreparably.tectonic\",\"risky.overextend.locator\"]}"
]


# In[51]:


import json
import pandas as pd
import subprocess
import concurrent.futures


# In[21]:


all_logs = {}

for log in logs:
    parsed_log = json.loads(log)
    assert 'green' in parsed_log and 'orange' in parsed_log
    if 'green' not in all_logs:
        all_logs['green'] = parsed_log['green']
    else:
        all_logs['green'].extend(parsed_log['green'])
    
    if 'orange' not in all_logs:
        all_logs['orange'] = parsed_log['orange']
    else:
        all_logs['orange'].extend(parsed_log['orange'])
    


# # In[22]:


# len(all_logs['green'] + all_logs['orange'])


# # In[23]:


# get_ipython().system('mkdir resumes')


# In[30]:


all_codes = pd.read_json("./reglists/checkin_codes.json")
all_students = pd.read_csv("../talentdaystudents_raw_10_11.csv")


# In[31]:


# all_codes


# In[34]:


all_students.rename(columns={"Hi {{field:479a780b-4131-4583-9519-9736b749a0d4}}, what's your email address?": "email"}, inplace=True)


# In[35]:


# all_students


# In[60]:


def download_resume(w3w):
    """Downloads a student's resume to ./resumes"""
    # Get student's resume URL from all_students
    email = all_codes[w3w][1]
    resume_url = all_students .query("""email == @email""")         .sort_values("Submitted At")         .iloc[0]['Please upload your resume here.']
    subprocess.run(f"wget {resume_url} -P ./resumes/", shell=True, check=True)
    print(f"Resume for {email} downloaded.")


list(map(download_resume, all_logs['green']))

list(map(download_resume, all_logs['orange']))


# In[ ]:




