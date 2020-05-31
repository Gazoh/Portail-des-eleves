import React, { useContext, useState } from "react";
import { Poll } from "../../../models/polls";
import "./polls-table.css";
import Card from "react-bootstrap/Card";

import { PollsBase } from "../PollsBase";
import { api } from "../../../services/apiService";
import { PollsLoading } from "../PollsLoading";
import { PollsError } from "../PollsError";
import { authService } from "../../../App";
import { ForbiddenError } from "../../utils/ErrorPage";
import { Pagination } from "../../utils/Pagination";
import { PollsTableFilter, PollStateFilter } from "./PollsTableFilter";
import { UserContext } from "../../../services/authService";
import { Table, useColumns } from "../../utils/table/Table";
import { PollEditModal } from "./PollEditModal";
import { Column } from "../../utils/table/TableHeader";
import { PageTitle } from "../../utils/PageTitle";
import { sortingToApiParameter } from "../../utils/table/sorting";

export const PollsTable = ({
    adminVersion,
    columnData,
}: {
    adminVersion: boolean;
    columnData: (setEditPoll) => Column[];
}) => {
    const user = useContext(UserContext);

    // Only filter by user for the non admin version.
    const userFilter = () => (!adminVersion && user ? user.id : undefined);

    // Contains the poll currently edited in the modal.
    const [editPoll, setEditPoll] = useState<Poll | null>(null);

    // Create the sorting.
    const { columns, sorting } = useColumns<Poll>(columnData(setEditPoll));

    // By default, show all the polls to the simple users and only the polls to be reviewed to the admins.
    const defaultStateFilter: PollStateFilter = {
        accepted: !adminVersion,
        rejected: !adminVersion,
        reviewing: true,
    };

    const [stateFilter, setStateFilter] = useState<PollStateFilter>(
        defaultStateFilter
    );

    // `stateFilter` has to be transformed to an API parameter.
    const stateFilterToApiParameter = (stateFilter: PollStateFilter) => {
        const r: ("ACCEPTED" | "REJECTED" | "REVIEWING")[] = [];

        if (stateFilter.accepted) {
            r.push("ACCEPTED");
        }

        if (stateFilter.rejected) {
            r.push("REJECTED");
        }

        if (stateFilter.reviewing) {
            r.push("REVIEWING");
        }

        return r;
    };

    if (!authService.isStaff && adminVersion) {
        return <ForbiddenError />;
    }

    return (
        <PollsBase
            sidebarActions={
                <PollsTableFilter
                    defaultStateFilter={defaultStateFilter}
                    setStateFilter={setStateFilter}
                    formGroupProps={{ className: "mb-0" }}
                />
            }
        >
            <PageTitle>
                {adminVersion ? "Administration" : "Mes sondages"}
            </PageTitle>

            <Card>
                <Pagination
                    render={(polls: Poll[], paginationControl) => (
                        <>
                            <PollEditModal
                                show={editPoll !== null}
                                onHide={() => setEditPoll(null)}
                                poll={editPoll}
                                adminVersion={adminVersion}
                            />
                            <Table columns={columns} data={polls} />
                            {paginationControl}
                        </>
                    )}
                    apiKey={[
                        "polls.list",
                        {
                            user: userFilter(),
                            state: stateFilterToApiParameter(stateFilter),
                            ordering: sortingToApiParameter(sorting, {
                                question: "question",
                                publicationDate: "publication_date",
                                user: "user__pk",
                                state: "state",
                            }),
                        },
                    ]}
                    apiMethod={api.polls.list}
                    config={{ refetchOnWindowFocus: false }}
                    loadingElement={PollsLoading}
                    errorElement={PollsError}
                    paginationControlProps={{
                        className: "justify-content-center mt-5",
                    }}
                />
            </Card>
        </PollsBase>
    );
};
