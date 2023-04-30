import easing_functions
import typing as t


class Animatable:
    """Class for anything that should behave like `Animation` class"""
    
    def __init__(self):
        for required in ('ended', 'tick'):
            assert hasattr(self, required), 'Animatable should have {} var'.format(required)


class Pause(Animatable):
    def __init__(self, value: float, duration: float):
        """Adds pause between animations."""

        self.value = value
        self.duration = duration
        self.ended = False
        self.time = 0

        super().__init__()
    
    def tick(self, dt: float) -> float:
        self.time += dt
        if self.time >= self.duration:
            self.ended = True
        
        return self.value


class Animation(Animatable):
    def __init__(
        self, easing_type: t.Literal[
            "LinearInOut", "QuadEaseInOut", "QuadEaseIn",
            "QuadEaseOut", "CubicEaseInOut", "CubicEaseIn",
            "CubicEaseOut", "QuarticEaseInOut", "QuarticEaseIn",
            "QuarticEaseOut", "QuinticEaseInOut", "QuinticEaseIn",
            "QuinticEaseOut", "SineEaseInOut", "SineEaseIn",
            "SineEaseOut", "CircularEaseIn", "CircularEaseInOut",
            "CircularEaseOut", "ExponentialEaseInOut", "ExponentialEaseIn",
            "ExponentialEaseOut", "ElasticEaseIn", "ElasticEaseInOut",
            "ElasticEaseOut", "BackEaseIn", "BackEaseInOut",
            "BackEaseOut", "BounceEaseIn", "BounceEaseInOut", "BounceEaseOut",
        ],
        start_value: float, end_value: float, duration: float
    ):
        """
        Simple class for creating animations.
        Call `tick(dt)` method every frame to get new values according to
        chosen easing type. Once animation ends, `tick(dt)` method will be returning
        value corresponding to animation's max time (duration)

        Parameters
        ----------
        easing_type : str
            Easing type of animation
        start_value : float
            Starting value of the animation. Can be any float, greater or less that end_value
        end_value : float
            End value of the animation. Will be returned after duration of animation passed
        duration : float
            Duration of the animation, should be in milliseconds.
        """
        self.time = 0
        self.max_time = duration
        self.ended = False

        self.easing = getattr(easing_functions, easing_type)(
            start=start_value,
            end=end_value,
            duration=duration
        )

        self.max_value = end_value

        super().__init__()
    
    def tick(self, dt: float) -> float:
        """
        Calculates value correspoding to time of the animation.
        `dt` is time that passed since last call of `tick(dt)` method
        """
        self.time += dt
        
        if not self.ended and self.time >= self.max_time:
            self.ended = True

        if self.ended:
            return self.max_value
        else:
            return self.easing(self.time)


class Combo(Animatable):
    def __init__(
        self, animations: t.List[t.Tuple[any, Animatable]] | t.List[Animatable]
    ):
        """
        Class for chaining all passed animations

        Parameters
        ----------
        animations
            List of animations that should be chained.
            You can pass list of animations or list of tuples. First
            values of tuples will be used as `current_animation_name`
        """

        self.animations = animations
        
        if not isinstance(self.animations[0], tuple):
            self.animations = list(enumerate(self.animations))
        self.last_animation = len(self.animations) - 1

        self.ended = False
        self.value = None

        self.current_animation = 0
        self.current_animation_name = self.animations[self.current_animation][0]
    
    def tick(self, dt: float) -> float:
        if self.ended:
            return self.value

        value = self.animations[self.current_animation][1].tick(dt)

        if self.animations[self.current_animation][1].ended:
            if self.current_animation == self.last_animation:
                self.ended = True
                self.value = value

            else:
                self.current_animation += 1
                self.current_animation_name = self.animations[self.current_animation][0]
        
        return value