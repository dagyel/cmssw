import FWCore.ParameterSet.Config as cms

process = cms.Process("dqmFeeder")

process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'START70_V1::All'

process.load("FWCore.MessageService.MessageLogger_cfi")
# suppress printout of error messages on every event when a collection is missing in the event
process.MessageLogger.categories.append("EmDQMInvalidRefs")
process.MessageLogger.cerr.EmDQMInvalidRefs = cms.untracked.PSet(limit = cms.untracked.int32(5))

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/relval/CMSSW_7_0_0_pre8/RelValZEE/GEN-SIM-DIGI-RAW-HLTDEBUG/PU_START70_V1-v1/00000/1C634144-E94A-E311-964E-002618943866.root',
    )
)

process.load("HLTriggerOffline.Egamma.EgammaValidationAutoConf_cff")

# set output to verbose = all
process.dqmFeeder.verbosity = cms.untracked.uint32(3)
# switch to select between only MC matched histograms or all histograms
#process.dqmFeeder.mcMatchedOnly = cms.untracked.bool(False)
# switch for phi plots
process.dqmFeeder.noPhiPlots = cms.untracked.bool(False)
# switch for 2D isolation plots
process.dqmFeeder.noIsolationPlots = cms.untracked.bool(False)

process.p = cms.Path(
                     # require generated particles in fiducial volume
                     process.egammaSelectors *     
                     process.egammaValidationSequence
                    )

#----------------------------------------
process.post=cms.EDAnalyzer("EmDQMPostProcessor",
                            subDir = cms.untracked.string("HLT/HLTEgammaValidation"),
                            dataSet = cms.untracked.string("unknown"),
                            noPhiPlots = cms.untracked.bool(False),
                           )

#process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

#----------------------------------------
# DQM service
#----------------------------------------
process.load("DQMServices.Core.DQM_cfg")
process.load("DQMServices.Components.DQMEnvironment_cfi")
process.DQMStore.verbose = 0
process.DQM.collectorHost = ''
process.dqmSaver.convention = 'Online'
process.dqmSaver.saveByRun = 1
process.dqmSaver.saveAtJobEnd = True

process.ppost = cms.EndPath(process.post+process.dqmSaver)

#----------------------------------------
# End of original testEmDQMFeeder_cfg.py
#----------------------------------------
