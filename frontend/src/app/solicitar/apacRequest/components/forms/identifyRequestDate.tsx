import { FormRepository, FormProps } from "@/shared/repositories/formRepository";
import React from "react";
import CardForm from "@/shared/components/CardForm";
import { Box, Button, Typography } from "@mui/material";
import { formatDateToYMD, getFirstDays, getMonthNamePtBr } from "../../utils/dateUtils";
import { useFormRequest } from "../../contexts/FormApacRequest";

const IdentifyRequestDate = React.forwardRef<FormRepository, FormProps>((props, ref) => {
    const { form, disabled: disabledForm } = useFormRequest();
    const { setValue, getValues } = form;
    const [selectedDate, setSelectedDate] = React.useState<string>(() => getValues("requestDate") || "");
    const dates = getFirstDays(4);
    const disabled = props.disabled? props.disabled : disabledForm;

    const handleDateClick = (date: Date) => {
        const formatted = formatDateToYMD(date);
        setValue("requestDate", formatted);
        setSelectedDate(formatted);
    };

    React.useImperativeHandle(ref, ()=>({
        validate() {
            const requestDate = getValues("requestDate");
            if (!requestDate || requestDate === "") {
                return {success: false, message: "Selecione uma competência!"};
            }
            return { 
                success: true,
                message: "Formulário correto!"
            };
        },
    }));

    return (
        <CardForm title="Competência da APAC">
            <Box
                sx={{
                display: "flex",
                gap: 1,
                padding: disabled? 2:5,
                flexDirection: "column",
                flexWrap: "wrap",
                }}>
                {disabled?(
                    <Typography variant="h6" color="grey" sx={{textAlign: "center"}}>
                        {getMonthNamePtBr(selectedDate)}
                    </Typography>):(
                    <>
                    {dates.map((date, i) => {
                    const formatted = formatDateToYMD(date);
                    const isSelected = selectedDate === formatted;

                    return (
                        <Button
                        key={`box-date-${i}`}
                        onClick={() => handleDateClick(date)}
                        variant={isSelected ? "contained" : "outlined"}
                        color={isSelected ? "primary" : "inherit"}
                        sx={{
                            minWidth: 100,
                            fontWeight: isSelected ? "bold" : "normal",
                        }}
                        aria-selected={isSelected}
                        >
                        {getMonthNamePtBr(date)}
                        </Button>
                    );
                })}
                </>
                )}
            </Box>
        </CardForm>
    );
});

export default IdentifyRequestDate;
