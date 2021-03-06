import React from "react";
import { SidebarSeparator } from "../../../utils/sidebar/Sidebar";
import { SidebarSection } from "../../../utils/sidebar/SidebarSection";
import { CheckboxField } from "../../../utils/sidebar/CheckboxField";
import { Link } from "react-router-dom";

export type ListEventsSidebarParameters = {
    time: {
        before: boolean;
        now: boolean;
        after: boolean;
    };
};

export const ListEventsSidebar = ({
    associationId,
    parameters,
    setParameters,
    adminVersion,
}: {
    associationId: string;
    parameters: ListEventsSidebarParameters;
    setParameters: (
        value:
            | ((
                  prevState: ListEventsSidebarParameters
              ) => ListEventsSidebarParameters)
            | ListEventsSidebarParameters
    ) => void;
    adminVersion: boolean;
}) => (
    <>
        <SidebarSeparator />
        <SidebarSection
            retractable={false}
            title="Voir les événements..."
            retractedByDefault={false}
        >
            <CheckboxField
                label={"Terminés"}
                state={parameters.time["before"]}
                onChange={(newTime) =>
                    setParameters({ ...parameters, time: newTime })
                }
            />
            <CheckboxField
                label={"En cours"}
                state={parameters.time["now"]}
                onChange={(newTime) =>
                    setParameters({ ...parameters, time: newTime })
                }
            />
            <CheckboxField
                label={"À venir"}
                state={parameters.time["after"]}
                onChange={(newTime) =>
                    setParameters({ ...parameters, time: newTime })
                }
            />
        </SidebarSection>
        {adminVersion && (
            <>
                <SidebarSeparator />
                <Link
                    className="btn btn-outline-primary"
                    to={`/associations/${associationId}/evenements/nouveau`}
                >
                    Nouvel événement
                </Link>
            </>
        )}
    </>
);
