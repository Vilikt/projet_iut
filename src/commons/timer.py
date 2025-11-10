class Timer:
    def __init__(self, time_to_wait: float, loop: bool = True, auto_start: bool = True):
        """
        Initialise le timer.

        Args:
            time_to_wait: Temps d'attente en millisecondes (doit être > 0)
            loop: Si True, le timer se réinitialise automatiquement après chaque cycle
            auto_start: Si True, le timer démarre immédiatement à l'initialisation
        """
        self.time_to_wait = time_to_wait  # Utilise le setter pour la validation
        self.__time_elapsed = 0.0  # Temps écoulé en millisecondes
        self.__finished = False   # État de fin de cycle
        self.__loop = loop        # Mode boucle
        self.__running = auto_start  # État d'exécution

    def __deepcopy__(self, memo):
        # 1. Crée une nouvelle instance sans appeler __init__ (pour éviter les validations inutiles)
        copie = self.__class__.__new__(self.__class__)

        # 2. Enregistre la copie dans memo pour gérer les références circulaires
        memo[id(self)] = copie

        # 3. Copie chaque attribut privé
        copie.__time_to_wait = self.__time_to_wait  # On accède directement à l'attribut privé
        copie.__time_elapsed = self.__time_elapsed
        copie.__finished = self.__finished
        copie.__loop = self.__loop
        copie.__running = self.__running

        return copie

    @property
    def time_to_wait(self) -> float:
        """Temps d'attente configuré (en millisecondes)."""
        return self.__time_to_wait

    @time_to_wait.setter
    def time_to_wait(self, time_to_wait: float):
        if time_to_wait <= 0:
            raise ValueError("Le temps d'attente doit être positif")
        self.__time_to_wait = time_to_wait

    @property
    def time_elapsed(self) -> float:
        """Temps écoulé depuis le dernier démarrage/redémarrage (en millisecondes)."""
        return self.__time_elapsed

    @property
    def progress(self) -> float:
        """Progression du timer entre 0.0 et 1.0."""
        return min(self.__time_elapsed / self.time_to_wait, 1.0)

    @property
    def remaining(self) -> float:
        """Temps restant avant la fin du cycle actuel (en millisecondes)."""
        return max(self.time_to_wait - self.__time_elapsed, 0.0)

    @property
    def finished(self) -> bool:
        """True si le timer a atteint ou dépassé time_to_wait."""
        return self.__finished

    @property
    def running(self) -> bool:
        """True si le timer est en cours d'exécution."""
        return self.__running

    def __repr__(self) -> str:
        return (f"Timer(time_to_wait={self.time_to_wait}ms, elapsed={self.__time_elapsed:.2f}ms, "
                f"running={self.__running}, finished={self.__finished}, loop={self.__loop})")

    def start(self):
        """Démarre ou reprend le timer.
        Pour un timer one-shot déjà terminé, cette méthode n'a aucun effet."""
        if not self.__loop and self.__finished:
            return
        self.__running = True

    def restart(self):
        """Réinitialise le timer et le démarre."""
        self.__time_elapsed = 0.0
        self.__finished = False
        self.__running = True

    def pause(self):
        """Met en pause le timer. Peut être repris avec start()."""
        self.__running = False

    def stop(self):
        """Arrête complètement le timer et le réinitialise."""
        self.__running = False
        self.__time_elapsed = 0.0
        self.__finished = False

    def reset(self):
        """Réinitialise le timer sans le démarrer."""
        self.__time_elapsed = 0.0
        self.__finished = False

    def update(self, delta: float):
        """
        Met à jour le timer.

        Args:
            delta: Temps écoulé depuis le dernier update (en millisecondes).
                   Doit être positif.
        """
        if delta <= 0:
            return  # Ignorer les valeurs non valides

        if not self.__running:
            return

        # Réinitialiser l'état "fini" en mode boucle avant de mettre à jour
        if self.__loop and self.__finished:
            self.__finished = False

        self.__time_elapsed += delta

        # Vérifier si le temps est écoulé
        if self.__time_elapsed >= self.time_to_wait:
            self.__finished = True
            if self.__loop:
                self.__time_elapsed = 0.0
                # Note: On ne réinitialise pas __finished ici pour permettre
                # la détection de la fin de cycle même en mode boucle
            else:
                self.__running = False
