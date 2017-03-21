from __future__ import absolute_import, unicode_literals
from wikigenomes.settings import BASE_DIR
from celery import shared_task
from scripts import jbrowse_configuration
from scripts import flatfile_ingestion

import os
final_tids = {
'224326',
'160488',
'272624',
'122586',
'511145',
'214092',
'160490',
'83332',
'36809',
'765698',
'446465',
'525903',
'759362',
'565050',
'515635'
}
org_taxids = [
    # '107806',
    # '224326',
    # '243275',
    # '189518',
    # '192222',
    # '85962',
    # '177416',
    # '300852',
    # '208964',
    # '160488',
    # '205918',
    # '190485',
    # '394',
    # '266834',
    # '272624',
    # '242231',
    # '122586',
    # '568707',
    # '1208660',
    # '257313',
    # '1028307',
    # '716541',
    # '511145',
    # '386585',
    # '585056',
    # '585057',
    # '685038',
    # '1133852',
    # '1125630',
    # '300267',
    # '198214',
    # '393305',
    # '214092',
    # '380703',
    # '243277',
    # '312309',
    # '223926',
    # '71421',
    # '227377',
    # '272947',
    # '272561',
    # '471472',
    # '295405',
    # '226186',
    # '190304',
    # '882',
    # '272943',
    # '269796',
    # '194439',
    # '324602',
    # '167539',
    # '93061',
    # '176280',
    # '243230',
    # '388919',
    # '568814',
    # '210007',
    # '208435',
    # '171101',
    # '160490',
    # '226185',
    # '333849',
    # '272623',
    # '198094',
    # '260799',
    # '226900',
    # '224308',
    # '281309',
    # '272562',
    # '441771',
    # '413999',
    # '272563',
    # '264732',
    # '272621',
    # '220668',
    # '321967',
    # '362948',
    # '169963',
    # '702459',
    # '196627',
    # '233413',
    # '272631',
    # '246196',
    # '83332',
    # '100226',
    # '272632',
    # '272634',
    # '265311',
    # '243274',
    # '525284',
    # '243160',
    # '365659',
    # '289376',
    # '272560',
    # '99287',
    # '220341',
    # '251221',
    # '749927',
    # '243231',
    # '36809',
    # '765698',
    # '446465',
    # '871585',
    # '224324',
    # '211586',
    # '525903',
    # '115713',
    # '759362',
    # '402612',
    # '366394',
    # '197221',
    # '309807',
    # '190650',
    # '565050',
    # '206672',
    # '223283',
    # '243090',
    # '515635',
    # '176299',
    # '224911'
]


@shared_task
def get_wd_genome_data():
    """
    gather genomic data and configures genome level feature tracks for jbrowse
    :return:
    """
    taskLog = []
    for taxid in org_taxids:
        refObj = jbrowse_configuration.GenomeDataRetrieval(taxid=taxid)
        taskLog.append(refObj.get_assembly_summary())
        taskLog.append(refObj.generate_reference())
        taskLog.append(refObj.generate_tracklist())
    return taskLog


@shared_task
def get_wd_features():
    """
    gather feature data and configures .gff files for jbrowse
    :return:
    """
    taskLog = []
    for taxid in org_taxids:
        refObj = jbrowse_configuration.FeatureDataRetrieval(taxid=taxid)
        taskLog.append(refObj.get_wd_genes())
        taskLog.append(refObj.get_wd_operons())
        # taskLog.append(refObj.get_mutants())
        taskLog.append(refObj.genes2gff())
        taskLog.append(refObj.operons2gff())
        # taskLog.append(refObj.mutants2gff())
    return taskLog


@shared_task
def update_orthologues():
    """
    converts orthologue csv flatfile to mongo to json for application usage
    :return:
    """
    taskLog = []
    refObj = flatfile_ingestion.Flatfile2Mongo(fileName='chlamydia_locus_tag_lookup.csv')
    taskLog.append(refObj.ortho2mongo())
    taskLog.append(refObj.ortho_mongo2json())
    return taskLog


taskLog = []


for taxid in final_tids:
    print(taxid)
    refObj = jbrowse_configuration.FeatureDataRetrieval(taxid=taxid)
    taskLog.append(refObj.get_wd_genes())
    # taskLog.append(refObj.get_wd_operons())
    # # taskLog.append(refObj.get_mutants())
    taskLog.append(refObj.genes2gff())
    # taskLog.append(refObj.operons2gff())
    # # taskLog.append(refObj.mutants2gff())
    print(taskLog)
