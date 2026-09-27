"""SO-101 flow policy v1 as a LeRobot plugin. Importing this package registers policy type "so101flow".

    lerobot-train --policy.discover_packages_path=so101_policy --policy.type=so101flow ...
"""

from .configuration_so101flow import So101FlowConfig  # noqa: F401  (registers the config)
