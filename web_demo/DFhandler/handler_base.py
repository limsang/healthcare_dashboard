from abc import *

VALID_FILE_LIST = ['HeartRate.csv', 'BodyMass.csv', 'Workout.csv', 'StepCount.csv', 'DistanceCycling.csv', 'WalkingAsymmetryPercentage.csv', 'DistanceWalkingRunning.csv',
'RestingHeartRate.csv', 'SixMinuteWalkTestDistance.csv', 'Height.csv', 'VO2Max.csv', 'HKDataTypeSleepDurationGoal.csv', 'HeartRateVariabilitySDNN.csv',
'WalkingSpeed.csv', 'AppleExerciseTime.csv', 'BasalEnergyBurned.csv', 'AppleStandHour.csv', 'WalkingHeartRateAverage.csv', 'WalkingStepLength.csv',
'ActiveEnergyBurned.csv', 'HeadphoneAudioExposure.csv', 'WalkingDoubleSupportPercentage.csv', 'FlightsClimbed.csv', 'SleepAnalysis.csv', 'ActivitySummary.csv',
 'AppleStandTime.csv']

class BaseHandler(metaclass=ABCMeta):

    @abstractmethod
    def load_from_csv(self):
        pass

    @abstractmethod
    def preproc(self):
        pass

    @abstractmethod
    def analysis_with_model(self):
        pass

    @abstractmethod
    def visualize(self):
        pass




